# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from .create_event_request_body_event_type import CreateEventRequestBodyEventType
from .event_body import EventBody


class CreateEventRequestBody(UniversalBaseModel):
    body: typing.Optional[EventBody] = None
    event_type: CreateEventRequestBodyEventType = pydantic.Field()
    """
    Either 'identify' or 'track'
    """

    sent_at: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    Optionally provide a timestamp at which the event was sent to Schematic
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
