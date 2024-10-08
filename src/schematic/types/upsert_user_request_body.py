# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
import datetime as dt
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class UpsertUserRequestBody(UniversalBaseModel):
    company: typing.Dict[str, str] = pydantic.Field()
    """
    Optionally specify company using key/value pairs
    """

    company_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Optionally specify company using Schematic company ID
    """

    id: typing.Optional[str] = pydantic.Field(default=None)
    """
    If you know the Schematic ID, you can use that here instead of keys
    """

    keys: typing.Dict[str, str]
    last_seen_at: typing.Optional[dt.datetime] = None
    name: typing.Optional[str] = None
    traits: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = pydantic.Field(default=None)
    """
    A map of trait names to trait values
    """

    update_only: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
