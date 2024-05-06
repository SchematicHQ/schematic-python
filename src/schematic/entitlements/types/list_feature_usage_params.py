# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import pydantic_v1


class ListFeatureUsageParams(pydantic_v1.BaseModel):
    """
    Input parameters
    """

    company_id: typing.Optional[str] = None
    company_keys: typing.Optional[typing.Dict[str, typing.Any]] = None
    feature_ids: typing.Optional[typing.List[str]] = None
    limit: typing.Optional[int] = None
    offset: typing.Optional[int] = None
    q: typing.Optional[str] = None

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
