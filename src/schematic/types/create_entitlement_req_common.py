# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .create_entitlement_req_common_metric_period import (
    CreateEntitlementReqCommonMetricPeriod,
)
from .create_entitlement_req_common_metric_period_month_reset import (
    CreateEntitlementReqCommonMetricPeriodMonthReset,
)
from .create_entitlement_req_common_value_type import (
    CreateEntitlementReqCommonValueType,
)
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class CreateEntitlementReqCommon(UniversalBaseModel):
    feature_id: str
    metric_period: typing.Optional[CreateEntitlementReqCommonMetricPeriod] = None
    metric_period_month_reset: typing.Optional[CreateEntitlementReqCommonMetricPeriodMonthReset] = None
    value_bool: typing.Optional[bool] = None
    value_numeric: typing.Optional[int] = None
    value_trait_id: typing.Optional[str] = None
    value_type: CreateEntitlementReqCommonValueType

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
