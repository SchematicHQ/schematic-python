# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class BillingCustomerResponseData(UniversalBaseModel):
    """
    The created resource
    """

    company_id: typing.Optional[str] = None
    deleted_at: typing.Optional[dt.datetime] = None
    email: str
    external_id: str
    failed_to_import: bool
    id: str
    name: str
    updated_at: dt.datetime

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
