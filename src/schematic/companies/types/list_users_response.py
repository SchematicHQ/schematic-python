# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...types.user_detail_response_data import UserDetailResponseData
from .list_users_params import ListUsersParams


class ListUsersResponse(UniversalBaseModel):
    data: typing.List[UserDetailResponseData] = pydantic.Field()
    """
    The returned resources
    """

    params: ListUsersParams = pydantic.Field()
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
