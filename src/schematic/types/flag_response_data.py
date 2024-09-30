# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import datetime as dt
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class FlagResponseData(UniversalBaseModel):
    created_at: dt.datetime
    default_value: bool
    description: str
    feature_id: typing.Optional[str] = None
    flag_type: str
    id: str
    key: str
    maintainer_id: typing.Optional[str] = None
    name: str
    updated_at: dt.datetime

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
