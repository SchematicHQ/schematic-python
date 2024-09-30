# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
from ...types.user_detail_response_data import UserDetailResponseData
from .lookup_user_params import LookupUserParams
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class LookupUserResponse(UniversalBaseModel):
    data: UserDetailResponseData
    params: LookupUserParams = pydantic.Field()
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
