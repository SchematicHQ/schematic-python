# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import datetime as dt
import typing
from .feature_response_data import FeatureResponseData
from .billing_price_view import BillingPriceView
from .plan_response_data import PlanResponseData
from .entity_trait_definition_response_data import EntityTraitDefinitionResponseData
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class PlanEntitlementResponseData(UniversalBaseModel):
    created_at: dt.datetime
    environment_id: str
    feature: typing.Optional[FeatureResponseData] = None
    feature_id: str
    id: str
    metered_monthly_price: typing.Optional[BillingPriceView] = None
    metered_yearly_price: typing.Optional[BillingPriceView] = None
    metric_period: typing.Optional[str] = None
    metric_period_month_reset: typing.Optional[str] = None
    plan: typing.Optional[PlanResponseData] = None
    plan_id: str
    price_behavior: typing.Optional[str] = None
    rule_id: str
    updated_at: dt.datetime
    value_bool: typing.Optional[bool] = None
    value_numeric: typing.Optional[int] = None
    value_trait: typing.Optional[EntityTraitDefinitionResponseData] = None
    value_trait_id: typing.Optional[str] = None
    value_type: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
