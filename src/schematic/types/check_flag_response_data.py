# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class CheckFlagResponseData(UniversalBaseModel):
    """
    The returned resource
    """

    company_id: typing.Optional[str] = None
    error: typing.Optional[str] = None
    reason: str
    rule_id: typing.Optional[str] = None
    user_id: typing.Optional[str] = None
    value: bool

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
