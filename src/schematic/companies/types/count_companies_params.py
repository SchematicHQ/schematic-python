# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class CountCompaniesParams(pydantic_v1.BaseModel):
    """
    Input parameters
    """

    ids: typing.Optional[typing.List[str]] = None
    limit: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    Page limit (default 100)
    """

    offset: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    Page offset (default 0)
    """

    plan_id: typing.Optional[str] = None
    q: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Search filter
    """

    without_feature_override_for: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Filter out companies that already have a company override for the specified feature ID
    """

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
