# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from .preview_object import PreviewObject


class EventDetailResponseData(UniversalBaseModel):
    api_key: typing.Optional[str] = None
    body: typing.Dict[str, typing.Optional[typing.Any]]
    body_preview: str
    captured_at: dt.datetime
    company: typing.Optional[PreviewObject] = None
    company_id: typing.Optional[str] = None
    enriched_at: typing.Optional[dt.datetime] = None
    environment_id: typing.Optional[str] = None
    error_message: typing.Optional[str] = None
    feature_ids: typing.List[str]
    features: typing.List[PreviewObject]
    id: str
    loaded_at: typing.Optional[dt.datetime] = None
    processed_at: typing.Optional[dt.datetime] = None
    quantity: int
    sent_at: typing.Optional[dt.datetime] = None
    status: str
    subtype: typing.Optional[str] = None
    type: str
    updated_at: dt.datetime
    user: typing.Optional[PreviewObject] = None
    user_id: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
