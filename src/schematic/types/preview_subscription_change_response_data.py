# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import datetime as dt
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class PreviewSubscriptionChangeResponseData(UniversalBaseModel):
    """
    The requested resource
    """

    amount_off: int
    due_now: int
    new_charges: int
    percent_off: float
    period_start: dt.datetime
    promo_code_applied: bool
    proration: int
    trial_end: typing.Optional[dt.datetime] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
