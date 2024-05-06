# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import pydantic_v1


class ApiKeyRequestListResponseData(pydantic_v1.BaseModel):
    api_key_id: str
    ended_at: typing.Optional[dt.datetime] = None
    environment_id: typing.Optional[str] = None
    id: str
    method: str
    req_body: typing.Optional[str] = None
    request_type: typing.Optional[str] = None
    resource_id: typing.Optional[int] = None
    resource_id_string: typing.Optional[str] = None
    resource_name: typing.Optional[str] = None
    resource_type: typing.Optional[str] = None
    resp_code: typing.Optional[int] = None
    secondary_resource: typing.Optional[str] = None
    started_at: dt.datetime
    url: str
    user_name: typing.Optional[str] = None

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
