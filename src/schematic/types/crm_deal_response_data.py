# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class CrmDealResponseData(UniversalBaseModel):
    """
    The created resource
    """

    account_id: str
    arr: str
    company_external_id: typing.Optional[str] = None
    created_at: dt.datetime
    deal_external_id: str
    deal_id: str
    environment_id: str
    mrr: str
    name: typing.Optional[str] = None
    product_external_id: typing.Optional[str] = None
    updated_at: dt.datetime

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
