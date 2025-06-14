# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from .billing_price_response_data import BillingPriceResponseData
from .billing_product_detail_response_data import BillingProductDetailResponseData
from .custom_plan_config import CustomPlanConfig
from .feature_detail_response_data import FeatureDetailResponseData
from .plan_entitlement_response_data import PlanEntitlementResponseData


class CompanyPlanDetailResponseData(UniversalBaseModel):
    audience_type: typing.Optional[str] = None
    billing_product: typing.Optional[BillingProductDetailResponseData] = None
    charge_type: str
    company_can_trial: bool
    company_count: int
    controlled_by: str
    created_at: dt.datetime
    current: bool
    custom: bool
    custom_plan_config: typing.Optional[CustomPlanConfig] = None
    description: str
    entitlements: typing.List[PlanEntitlementResponseData]
    features: typing.List[FeatureDetailResponseData]
    icon: str
    id: str
    is_custom: bool
    is_default: bool
    is_free: bool
    is_trialable: bool
    monthly_price: typing.Optional[BillingPriceResponseData] = None
    name: str
    one_time_price: typing.Optional[BillingPriceResponseData] = None
    plan_type: str
    trial_days: typing.Optional[int] = None
    updated_at: dt.datetime
    valid: bool
    yearly_price: typing.Optional[BillingPriceResponseData] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
