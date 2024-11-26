# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .billing_product_detail_response_data import BillingProductDetailResponseData
import datetime as dt
from .plan_entitlement_response_data import PlanEntitlementResponseData
from .feature_detail_response_data import FeatureDetailResponseData
from .billing_price_response_data import BillingPriceResponseData
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class PlanGroupPlanDetailResponseData(UniversalBaseModel):
    audience_type: typing.Optional[str] = None
    billing_product: typing.Optional[BillingProductDetailResponseData] = None
    company_count: int
    created_at: dt.datetime
    description: str
    entitlements: typing.List[PlanEntitlementResponseData]
    features: typing.List[FeatureDetailResponseData]
    icon: str
    id: str
    is_default: bool
    is_free: bool
    is_trialable: bool
    monthly_price: typing.Optional[BillingPriceResponseData] = None
    name: str
    plan_type: str
    trial_days: typing.Optional[int] = None
    updated_at: dt.datetime
    yearly_price: typing.Optional[BillingPriceResponseData] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
