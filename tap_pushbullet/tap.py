"""Pushbullet tap class."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_pushbullet import streams

if TYPE_CHECKING:
    from collections.abc import Sequence


class TapPushbullet(Tap):
    """Singer tap for Pushbullet."""

    name = "tap-pushbullet"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,
            description="API Key for Pushbullet",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> Sequence[Stream]:
        """Return a list of discovered streams."""
        return [
            streams.Chats(tap=self),
            streams.Devices(tap=self),
            streams.Pushes(tap=self),
            streams.Subscriptions(tap=self),
        ]
