# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
from ...types.event_summary_response_data import EventSummaryResponseData
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class GetEventSummaryBySubtypeResponse(UniversalBaseModel):
    data: EventSummaryResponseData
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
