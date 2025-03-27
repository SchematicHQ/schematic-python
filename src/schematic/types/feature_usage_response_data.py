# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from .feature_usage_response_data_allocation_type import FeatureUsageResponseDataAllocationType
import datetime as dt
from .feature_detail_response_data import FeatureDetailResponseData
from .billing_price_view import BillingPriceView
from .plan_response_data import PlanResponseData
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class FeatureUsageResponseData(UniversalBaseModel):
    access: bool = pydantic.Field()
    """
    Whether further usage is permitted.
    """

    allocation: typing.Optional[int] = pydantic.Field(default=None)
    """
    The maximum amount of usage that is permitted; a null value indicates that unlimited usage is permitted.
    """

    allocation_type: FeatureUsageResponseDataAllocationType = pydantic.Field()
    """
    The type of allocation that is being used.
    """

    entitlement_expiration_date: typing.Optional[dt.datetime] = None
    entitlement_id: str
    entitlement_type: str
    feature: typing.Optional[FeatureDetailResponseData] = None
    metric_reset_at: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    The time at which the metric will reset.
    """

    month_reset: typing.Optional[str] = pydantic.Field(default=None)
    """
    If the period is current_month, when the month resets.
    """

    monthly_usage_based_price: typing.Optional[BillingPriceView] = None
    period: typing.Optional[str] = pydantic.Field(default=None)
    """
    The period over which usage is measured.
    """

    plan: typing.Optional[PlanResponseData] = None
    price_behavior: typing.Optional[str] = None
    soft_limit: typing.Optional[int] = pydantic.Field(default=None)
    """
    The soft limit for the feature usage. Available only for overage price behavior
    """

    usage: typing.Optional[int] = pydantic.Field(default=None)
    """
    The amount of usage that has been consumed; a null value indicates that usage is not being measured.
    """

    yearly_usage_based_price: typing.Optional[BillingPriceView] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
