# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import datetime as dt
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class WebhookResponseData(UniversalBaseModel):
    created_at: dt.datetime
    id: str
    name: str
    request_types: typing.List[str]
    secret: str
    status: str
    updated_at: dt.datetime
    url: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
