# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...types.crm_product_response_data import CrmProductResponseData
import pydantic
from .list_crm_products_params import ListCrmProductsParams
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ListCrmProductsResponse(UniversalBaseModel):
    data: typing.List[CrmProductResponseData] = pydantic.Field()
    """
    The returned resources
    """

    params: ListCrmProductsParams = pydantic.Field()
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
