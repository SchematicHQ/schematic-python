# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
from ...types.event_detail_response_data import EventDetailResponseData
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class GetEventResponse(UniversalBaseModel):
    data: EventDetailResponseData
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
