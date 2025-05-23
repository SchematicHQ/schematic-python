# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class UsageBasedEntitlementRequestBody(UniversalBaseModel):
    currency: typing.Optional[str] = None
    monthly_metered_price_id: typing.Optional[str] = None
    monthly_unit_price: typing.Optional[int] = None
    monthly_unit_price_decimal: typing.Optional[str] = None
    overage_billing_product_id: typing.Optional[str] = None
    price_behavior: typing.Optional[str] = None
    soft_limit: typing.Optional[int] = None
    yearly_metered_price_id: typing.Optional[str] = None
    yearly_unit_price: typing.Optional[int] = None
    yearly_unit_price_decimal: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
