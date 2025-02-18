# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .update_add_on_request_body import UpdateAddOnRequestBody
from .update_pay_in_advance_request_body import UpdatePayInAdvanceRequestBody
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ChangeSubscriptionInternalRequestBody(UniversalBaseModel):
    add_on_ids: typing.List[UpdateAddOnRequestBody]
    company_id: str
    coupon_external_id: typing.Optional[str] = None
    new_plan_id: str
    new_price_id: str
    pay_in_advance: typing.List[UpdatePayInAdvanceRequestBody]
    payment_method_id: typing.Optional[str] = None
    promo_code: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
