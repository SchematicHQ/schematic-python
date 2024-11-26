# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class PlanGroupResponseData(UniversalBaseModel):
    """
    The updated resource
    """

    add_on_ids: typing.List[str]
    default_plan_id: typing.Optional[str] = None
    id: str
    plan_ids: typing.List[str]
    trial_days: typing.Optional[int] = None
    trial_payment_method_required: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
