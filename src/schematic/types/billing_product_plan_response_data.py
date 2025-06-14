# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class BillingProductPlanResponseData(UniversalBaseModel):
    """
    The updated resource
    """

    account_id: str
    billing_product_id: str
    charge_type: str
    controlled_by: str
    environment_id: str
    is_trialable: bool
    monthly_price_id: typing.Optional[str] = None
    one_time_price_id: typing.Optional[str] = None
    plan_id: str
    trial_days: typing.Optional[int] = None
    yearly_price_id: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
