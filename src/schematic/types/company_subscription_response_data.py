# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import datetime as dt
from .billing_subscription_discount_view import BillingSubscriptionDiscountView
from .invoice_response_data import InvoiceResponseData
from .payment_method_response_data import PaymentMethodResponseData
from .billing_product_for_subscription_response_data import (
    BillingProductForSubscriptionResponseData,
)
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class CompanySubscriptionResponseData(UniversalBaseModel):
    cancel_at: typing.Optional[dt.datetime] = None
    cancel_at_period_end: bool
    currency: str
    customer_external_id: str
    discounts: typing.List[BillingSubscriptionDiscountView]
    expired_at: typing.Optional[dt.datetime] = None
    interval: str
    latest_invoice: typing.Optional[InvoiceResponseData] = None
    payment_method: typing.Optional[PaymentMethodResponseData] = None
    products: typing.List[BillingProductForSubscriptionResponseData]
    status: str
    subscription_external_id: str
    total_price: int
    trial_end: typing.Optional[dt.datetime] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
