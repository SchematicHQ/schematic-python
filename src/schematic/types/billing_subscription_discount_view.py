# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class BillingSubscriptionDiscountView(UniversalBaseModel):
    amount_off: typing.Optional[int] = None
    coupon_id: str
    coupon_name: str
    currency: typing.Optional[str] = None
    customer_facing_code: typing.Optional[str] = None
    discount_external_id: str
    duration: str
    duration_in_months: typing.Optional[int] = None
    ended_at: typing.Optional[dt.datetime] = None
    is_active: bool
    percent_off: typing.Optional[float] = None
    promo_code_external_id: typing.Optional[str] = None
    started_at: dt.datetime
    subscription_external_id: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
