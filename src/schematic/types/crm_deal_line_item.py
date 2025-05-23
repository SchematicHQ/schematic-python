# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from .decimal import Decimal


class CrmDealLineItem(UniversalBaseModel):
    billing_frequency: str
    created_at: dt.datetime
    currency: str
    description: str
    discount_percentage: typing.Optional[Decimal] = None
    id: str
    name: str
    price: float
    quantity: int
    term_month: typing.Optional[int] = None
    total_discount: typing.Optional[Decimal] = None
    updated_at: dt.datetime

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
