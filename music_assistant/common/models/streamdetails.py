"""Model(s) for streamdetails."""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Any

from mashumaro import DataClassDictMixin

from music_assistant.common.models.enums import MediaType
from music_assistant.common.models.media_items import AudioFormat


@dataclass(kw_only=True)
class LoudnessMeasurement(DataClassDictMixin):
    """Model for EBU-R128 loudness measurement details."""

    integrated: float
    true_peak: float
    lra: float
    threshold: float


@dataclass(kw_only=True)
class StreamDetails(DataClassDictMixin):
    """Model for streamdetails."""

    # NOTE: the actual provider/itemid of the streamdetails may differ
    # from the connected media_item due to track linking etc.
    # the streamdetails are only used to provide details about the content
    # that is going to be streamed.

    # mandatory fields
    provider: str
    item_id: str
    audio_format: AudioFormat
    media_type: MediaType = MediaType.TRACK

    # stream_title: radio streams can optionally set this field
    stream_title: str | None = None
    # duration of the item to stream, copied from media_item if omitted
    duration: int | None = None
    # total size in bytes of the item, calculated at eof when omitted
    size: int | None = None
    # expires: timestamp this streamdetails expire
    expires: float = time() + 3600
    # data: provider specific data (not exposed externally)
    data: Any = None
    # direct: if the url/file is supported by ffmpeg directly, use direct stream
    direct: str | None = None
    # can_seek: bool to indicate that the providers 'get_audio_stream' supports seeking of the item
    can_seek: bool = True

    # the fields below will be set/controlled by the streamcontroller
    loudness: LoudnessMeasurement | None = None
    queue_id: str | None = None
    seconds_streamed: float | None = None
    seconds_skipped: float | None = None
    target_loudness: float | None = None

    def __str__(self) -> str:
        """Return pretty printable string of object."""
        return self.uri

    def __post_serialize__(self, d: dict[Any, Any]) -> dict[Any, Any]:
        """Execute action(s) on serialization."""
        d.pop("queue_id", None)
        d.pop("seconds_streamed", None)
        d.pop("seconds_skipped", None)
        d.pop("target_loudness", None)
        return d

    @property
    def uri(self) -> str:
        """Return uri representation of item."""
        return f"{self.provider}://{self.media_type.value}/{self.item_id}"
