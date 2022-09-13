"""REST client handling, including PushbulletStream base class."""

from __future__ import annotations

from typing import Any

from singer_sdk import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator


class PushbulletStream(RESTStream):
    """Pushbullet stream class."""

    url_base = "https://api.pushbullet.com"
    next_page_token_jsonpath = "$.cursor"
    primary_keys = ["iden"]

    PAGE_SIZE = 100

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        api_key: str = self.config["api_key"]
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Access-Token",
            value=api_key,
            location="header",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        headers["User-Agent"] = f"{self.tap_name}/{self._tap.plugin_version}"
        return headers

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: str | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        params: dict = {
            "cursor": next_page_token,
            "limit": self.PAGE_SIZE,
            "modified_after": self.get_starting_replication_key_value(context),
        }
        return params
