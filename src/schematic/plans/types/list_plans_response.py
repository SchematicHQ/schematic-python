# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...types.plan_detail_response_data import PlanDetailResponseData
import pydantic
from .list_plans_params import ListPlansParams
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ListPlansResponse(UniversalBaseModel):
    data: typing.List[PlanDetailResponseData] = pydantic.Field()
    """
    The returned resources
    """

    params: ListPlansParams = pydantic.Field()
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
