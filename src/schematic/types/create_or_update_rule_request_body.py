# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from .create_or_update_condition_group_request_body import CreateOrUpdateConditionGroupRequestBody
from .create_or_update_condition_request_body import CreateOrUpdateConditionRequestBody
from .create_or_update_rule_request_body_rule_type import CreateOrUpdateRuleRequestBodyRuleType


class CreateOrUpdateRuleRequestBody(UniversalBaseModel):
    condition_groups: typing.List[CreateOrUpdateConditionGroupRequestBody]
    conditions: typing.List[CreateOrUpdateConditionRequestBody]
    id: typing.Optional[str] = None
    name: str
    priority: int
    rule_type: typing.Optional[CreateOrUpdateRuleRequestBodyRuleType] = None
    value: bool

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
