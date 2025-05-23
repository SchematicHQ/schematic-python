# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...types.feature_company_user_response_data import FeatureCompanyUserResponseData
from .list_feature_users_params import ListFeatureUsersParams


class ListFeatureUsersResponse(UniversalBaseModel):
    data: typing.List[FeatureCompanyUserResponseData] = pydantic.Field()
    """
    The returned resources
    """

    params: ListFeatureUsersParams = pydantic.Field()
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
