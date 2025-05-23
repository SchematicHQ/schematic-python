# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from .flag_response_data import FlagResponseData
from .rule_detail_response_data import RuleDetailResponseData


class RulesDetailResponseData(UniversalBaseModel):
    """
    The updated resource
    """

    flag: typing.Optional[FlagResponseData] = None
    rules: typing.List[RuleDetailResponseData]

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
