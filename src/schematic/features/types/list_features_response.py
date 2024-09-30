# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...types.feature_detail_response_data import FeatureDetailResponseData
import pydantic
from .list_features_params import ListFeaturesParams
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ListFeaturesResponse(UniversalBaseModel):
    data: typing.List[FeatureDetailResponseData] = pydantic.Field()
    """
    The returned resources
    """

    params: ListFeaturesParams = pydantic.Field()
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
