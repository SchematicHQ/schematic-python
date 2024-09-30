# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
from ...types.count_response import CountResponse
from .count_feature_companies_params import CountFeatureCompaniesParams
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class CountFeatureCompaniesResponse(UniversalBaseModel):
    data: CountResponse
    params: CountFeatureCompaniesParams = pydantic.Field()
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
