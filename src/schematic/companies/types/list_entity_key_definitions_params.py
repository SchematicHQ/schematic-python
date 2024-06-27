# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .list_entity_key_definitions_response_params_entity_type import ListEntityKeyDefinitionsResponseParamsEntityType


class ListEntityKeyDefinitionsParams(pydantic_v1.BaseModel):
    """
    Input parameters
    """

    entity_type: typing.Optional[ListEntityKeyDefinitionsResponseParamsEntityType] = None
    ids: typing.Optional[typing.List[str]] = None
    key: typing.Optional[str] = None
    limit: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    Page limit (default 100)
    """

    offset: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    Page offset (default 0)
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
