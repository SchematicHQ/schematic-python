# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...types.metric_counts_hourly_response_data import MetricCountsHourlyResponseData
import pydantic
from .list_metric_counts_params import ListMetricCountsParams
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ListMetricCountsResponse(UniversalBaseModel):
    data: typing.List[MetricCountsHourlyResponseData] = pydantic.Field()
    """
    The returned resources
    """

    params: ListMetricCountsParams = pydantic.Field()
    """
    Input parameters
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
