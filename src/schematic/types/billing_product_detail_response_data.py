# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import datetime as dt
import typing
from .billing_price_response_data import BillingPriceResponseData
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class BillingProductDetailResponseData(UniversalBaseModel):
    account_id: str
    created_at: dt.datetime
    currency: str
    environment_id: str
    external_id: str
    name: str
    price: float
    prices: typing.List[BillingPriceResponseData]
    product_id: str
    quantity: float
    subscription_count: int
    updated_at: dt.datetime

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
