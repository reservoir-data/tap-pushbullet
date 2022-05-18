"""Pushbullet tap class."""

from __future__ import annotations

from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from singer_sdk.streams import RESTStream

from tap_pushbullet.streams import Chats, Devices, Pushes, Subscriptions

STREAM_TYPES: list[type[RESTStream]] = [Chats, Devices, Pushes, Subscriptions]


class TapPushbullet(Tap):
    """Singer tap for Pushbullet."""

    name = "tap-pushbullet"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="API Key for Pushbullet",
        ),
        th.Property(
            "start_date",
            th.NumberType,
            description="Earliest Unix timestamp to get data from",
        ),
    ).to_dict()

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Pushbullet streams.
        """
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
