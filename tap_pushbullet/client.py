"""REST client handling, including PushbulletStream base class."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generator

import backoff
import requests
from requests_cache import install_cache
from singer_sdk import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.exceptions import RetriableAPIError
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import JSONPathPaginator, first

install_cache("tap_pushbullet_cache", backend="sqlite", expire_after=3600)


def _get_wait_time_from_response(exception: RetriableAPIError) -> float:
    if exception.response is None:
        return 60

    reset = exception.response.headers.get("X-Ratelimit-Reset")
    if reset:
        wait_time = float(reset) - datetime.now().timestamp()
        return max(wait_time, 0)

    return 0


class PushbulletPaginator(JSONPathPaginator):
    """Pushbullet API paginator."""

    def __init__(
        self,
        jsonpath: str,
        records_jsonpath: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize a Pushbullet paginator.

        Args:
            jsonpath: JSONPath expression to find the records.
            records_jsonpath: JSONPath expression to find the records.
            *args: Positional arguments to pass to the parent class.
            **kwargs: Keyword arguments to pass to the parent class.
        """
        super().__init__(jsonpath, *args, **kwargs)
        self.records_jsonpath = records_jsonpath

    def has_more(self, response: requests.Response) -> bool:
        """Return a boolean indicating whether there are more pages.

        Args:
            response: The response object.

        Returns:
            A boolean indicating whether there are more pages.
        """
        try:
            first(extract_jsonpath(self.records_jsonpath, response.json()))
        except StopIteration:
            return False

        return True


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

    def backoff_wait_generator(self) -> Generator[float, None, None]:
        """Get a backoff wait generator.

        Returns:
            A backoff wait generator.
        """
        return backoff.runtime(value=_get_wait_time_from_response)

    def get_new_paginator(self) -> PushbulletPaginator:
        """Get a new paginator.

        Returns:
            A new Pushbullet paginator.
        """
        return PushbulletPaginator(self.next_page_token_jsonpath, self.records_jsonpath)
