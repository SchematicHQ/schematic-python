# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class CreateOrUpdateFlagRequestBody(UniversalBaseModel):
    default_value: bool
    description: str
    feature_id: typing.Optional[str] = None
    flag_type: typing.Literal["boolean"] = "boolean"
    id: typing.Optional[str] = None
    key: str
    maintainer_id: typing.Optional[str] = None
    name: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
