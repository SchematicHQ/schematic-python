# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...types.billing_product_detail_response_data import (
    BillingProductDetailResponseData,
)
import pydantic
from .list_billing_products_params import ListBillingProductsParams
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ListBillingProductsResponse(UniversalBaseModel):
    data: typing.List[BillingProductDetailResponseData] = pydantic.Field()
    """
    The returned resources
    """

    params: ListBillingProductsParams = pydantic.Field()
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
