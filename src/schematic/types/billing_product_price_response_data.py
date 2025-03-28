# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import datetime as dt
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class BillingProductPriceResponseData(UniversalBaseModel):
    created_at: dt.datetime
    currency: str
    id: str
    interval: str
    is_active: bool
    meter_id: typing.Optional[str] = None
    price: int
    price_external_id: str
    product_external_id: str
    updated_at: dt.datetime
    usage_type: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
