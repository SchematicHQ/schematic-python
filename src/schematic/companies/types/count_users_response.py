# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
from ...types.count_response import CountResponse
from .count_users_params import CountUsersParams
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class CountUsersResponse(UniversalBaseModel):
    data: CountResponse
    params: CountUsersParams = pydantic.Field()
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
