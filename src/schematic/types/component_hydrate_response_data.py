# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .company_plan_detail_response_data import CompanyPlanDetailResponseData
from .usage_based_entitlement_response_data import UsageBasedEntitlementResponseData
from .component_capabilities import ComponentCapabilities
from .company_detail_response_data import CompanyDetailResponseData
from .component_response_data import ComponentResponseData
from .feature_usage_detail_response_data import FeatureUsageDetailResponseData
from .stripe_embed_info import StripeEmbedInfo
from .company_subscription_response_data import CompanySubscriptionResponseData
from .invoice_response_data import InvoiceResponseData
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ComponentHydrateResponseData(UniversalBaseModel):
    active_add_ons: typing.List[CompanyPlanDetailResponseData]
    active_plans: typing.List[CompanyPlanDetailResponseData]
    active_usage_based_entitlements: typing.List[UsageBasedEntitlementResponseData]
    capabilities: typing.Optional[ComponentCapabilities] = None
    company: typing.Optional[CompanyDetailResponseData] = None
    component: typing.Optional[ComponentResponseData] = None
    feature_usage: typing.Optional[FeatureUsageDetailResponseData] = None
    stripe_embed: typing.Optional[StripeEmbedInfo] = None
    subscription: typing.Optional[CompanySubscriptionResponseData] = None
    upcoming_invoice: typing.Optional[InvoiceResponseData] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
