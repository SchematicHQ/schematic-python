# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import typing_extensions
from ..core.serialization import FieldMetadata
import datetime as dt
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class PaymentMethodResponseData(UniversalBaseModel):
    card_brand: typing.Optional[str] = None
    card_exp_month: typing.Optional[int] = None
    card_exp_year: typing.Optional[int] = None
    card_last_4: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="card_last4")] = None
    company_id: typing.Optional[str] = None
    created_at: dt.datetime
    customer_external_id: str
    environment_id: str
    external_id: str
    id: str
    payment_method_type: str
    subscription_external_id: typing.Optional[str] = None
    updated_at: dt.datetime

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
