# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import datetime as dt
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class EventSummaryResponseData(UniversalBaseModel):
    company_count: int
    environment_id: str
    event_count: int
    event_subtype: str
    last_seen_at: typing.Optional[dt.datetime] = None
    user_count: int

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
