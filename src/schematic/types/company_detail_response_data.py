# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .company_plan_with_billing_sub_view import CompanyPlanWithBillingSubView
from .billing_subscription_view import BillingSubscriptionView
import datetime as dt
from .entity_trait_detail_response_data import EntityTraitDetailResponseData
from .entity_key_detail_response_data import EntityKeyDetailResponseData
from .company_event_period_metrics_response_data import (
    CompanyEventPeriodMetricsResponseData,
)
from .payment_method_response_data import PaymentMethodResponseData
from .generic_preview_object import GenericPreviewObject
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class CompanyDetailResponseData(UniversalBaseModel):
    add_ons: typing.List[CompanyPlanWithBillingSubView]
    billing_subscription: typing.Optional[BillingSubscriptionView] = None
    billing_subscriptions: typing.List[BillingSubscriptionView]
    created_at: dt.datetime
    entity_traits: typing.List[EntityTraitDetailResponseData]
    environment_id: str
    id: str
    keys: typing.List[EntityKeyDetailResponseData]
    last_seen_at: typing.Optional[dt.datetime] = None
    logo_url: typing.Optional[str] = None
    metrics: typing.List[CompanyEventPeriodMetricsResponseData]
    name: str
    payment_methods: typing.List[PaymentMethodResponseData]
    plan: typing.Optional[CompanyPlanWithBillingSubView] = None
    plans: typing.List[GenericPreviewObject]
    traits: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = pydantic.Field(default=None)
    """
    A map of trait names to trait values
    """

    updated_at: dt.datetime
    user_count: int

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
