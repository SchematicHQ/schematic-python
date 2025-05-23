# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class CompanyEventPeriodMetricsResponseData(UniversalBaseModel):
    account_id: str
    captured_at_max: dt.datetime
    captured_at_min: dt.datetime
    company_id: str
    created_at: dt.datetime
    environment_id: str
    event_subtype: str
    month_reset: str
    period: str
    valid_until: typing.Optional[dt.datetime] = None
    value: int

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
