# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class CountComponentsParams(UniversalBaseModel):
    """
    Input parameters
    """

    limit: typing.Optional[int] = pydantic.Field(default=None)
    """
    Page limit (default 100)
    """

    offset: typing.Optional[int] = pydantic.Field(default=None)
    """
    Page offset (default 0)
    """

    q: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow