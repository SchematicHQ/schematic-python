# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
from ...types.check_flags_response_data import CheckFlagsResponseData
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class CheckFlagsResponse(UniversalBaseModel):
    data: CheckFlagsResponseData
    params: typing.Dict[str, typing.Optional[typing.Any]] = pydantic.Field()
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
