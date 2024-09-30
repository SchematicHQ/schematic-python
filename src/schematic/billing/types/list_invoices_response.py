# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...types.invoice_response_data import InvoiceResponseData
import pydantic
from .list_invoices_params import ListInvoicesParams
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ListInvoicesResponse(UniversalBaseModel):
    data: typing.List[InvoiceResponseData] = pydantic.Field()
    """
    The returned resources
    """

    params: ListInvoicesParams = pydantic.Field()
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
