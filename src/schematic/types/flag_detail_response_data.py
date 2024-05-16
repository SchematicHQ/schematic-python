# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .feature_response_data import FeatureResponseData
from .flag_check_log_response_data import FlagCheckLogResponseData
from .rule_detail_response_data import RuleDetailResponseData


class FlagDetailResponseData(pydantic_v1.BaseModel):
    created_at: dt.datetime
    default_value: bool
    description: str
    feature: typing.Optional[FeatureResponseData] = None
    feature_id: typing.Optional[str] = None
    flag_type: str
    id: str
    key: str
    latest_check: typing.Optional[FlagCheckLogResponseData] = None
    name: str
    rules: typing.List[RuleDetailResponseData]
    updated_at: dt.datetime

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
