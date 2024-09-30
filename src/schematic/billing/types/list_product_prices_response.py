# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...types.billing_price_response_data import BillingPriceResponseData
import pydantic
from .list_product_prices_params import ListProductPricesParams
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ListProductPricesResponse(UniversalBaseModel):
    data: typing.List[BillingPriceResponseData] = pydantic.Field()
    """
    The returned resources
    """

    params: ListProductPricesParams = pydantic.Field()
    """
    Input parameters
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
