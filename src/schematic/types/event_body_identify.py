# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .event_body_identify_company import EventBodyIdentifyCompany


class EventBodyIdentify(pydantic_v1.BaseModel):
    company: typing.Optional[EventBodyIdentifyCompany] = pydantic_v1.Field(default=None)
    """
    Information about the company associated with the user; required only if it is a new user
    """

    keys: typing.Dict[str, typing.Any] = pydantic_v1.Field()
    """
    Key-value pairs to identify the user
    """

    name: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    The display name of the user being identified; required only if it is a new user
    """

    traits: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(default=None)
    """
    A map of user trait names to trait values
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
