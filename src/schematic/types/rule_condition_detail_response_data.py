# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .entity_trait_definition_response_data import EntityTraitDefinitionResponseData
import datetime as dt
from .preview_object_response_data import PreviewObjectResponseData
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class RuleConditionDetailResponseData(UniversalBaseModel):
    comparison_trait: typing.Optional[EntityTraitDefinitionResponseData] = None
    comparison_trait_id: typing.Optional[str] = None
    condition_group_id: typing.Optional[str] = None
    condition_type: str
    created_at: dt.datetime
    environment_id: str
    event_subtype: typing.Optional[str] = None
    flag_id: typing.Optional[str] = None
    id: str
    metric_period: typing.Optional[str] = None
    metric_period_month_reset: typing.Optional[str] = None
    metric_value: typing.Optional[int] = None
    operator: str
    plan_id: typing.Optional[str] = None
    resource_ids: typing.List[str]
    resources: typing.List[PreviewObjectResponseData]
    rule_id: str
    trait: typing.Optional[EntityTraitDefinitionResponseData] = None
    trait_entity_type: typing.Optional[str] = None
    trait_id: typing.Optional[str] = None
    trait_value: str
    updated_at: dt.datetime

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
