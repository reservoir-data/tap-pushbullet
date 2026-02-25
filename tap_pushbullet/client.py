"""REST client handling, including PushbulletStream base class."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, override

import backoff
from requests_cache import install_cache
from singer_sdk import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator

if TYPE_CHECKING:
    from collections.abc import Generator

    from singer_sdk.exceptions import RetriableAPIError
    from singer_sdk.helpers.types import Context

install_cache("tap_pushbullet_cache", backend="sqlite", expire_after=3600)


def _get_wait_time_from_response(exception: RetriableAPIError) -> float:
    if exception.response is None:
        return 60

    if reset := exception.response.headers.get("X-Ratelimit-Reset"):
        wait_time = float(reset) - datetime.now(tz=UTC).timestamp()
        return max(wait_time, 0)

    return 0


class PushbulletStream(RESTStream[str]):
    """Pushbullet stream class."""

    url_base = "https://api.pushbullet.com"
    next_page_token_jsonpath = "$.cursor"  # noqa: S105
    primary_keys = ("iden",)

    PAGE_SIZE = 100

    @override
    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        return APIKeyAuthenticator(
            key="Access-Token",
            value=self.config["api_key"],
            location="header",
        )

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        modified_after: float | None = self.get_starting_replication_key_value(context)

        if not modified_after and (start_date_str := self.config.get("start_date")):
            modified_after = datetime.fromisoformat(start_date_str).timestamp()

        return {
            "cursor": next_page_token,
            "limit": self.PAGE_SIZE,
            "modified_after": modified_after,
        }

    @override
    def backoff_wait_generator(self) -> Generator[float, None, None]:
        """Get a backoff wait generator.

        Returns:
            A backoff wait generator.
        """
        return backoff.runtime(value=_get_wait_time_from_response)
