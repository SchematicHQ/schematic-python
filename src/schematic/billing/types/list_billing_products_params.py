# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ListBillingProductsParams(UniversalBaseModel):
    """
    Input parameters
    """

    ids: typing.Optional[typing.List[str]] = None
    limit: typing.Optional[int] = pydantic.Field(default=None)
    """
    Page limit (default 100)
    """

    name: typing.Optional[str] = None
    offset: typing.Optional[int] = pydantic.Field(default=None)
    """
    Page offset (default 0)
    """

    price_usage_type: typing.Optional[str] = None
    q: typing.Optional[str] = None
    with_prices_only: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Filter products that have prices
    """

    with_zero_price: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Filter products that have zero price for free subscription type
    """

    without_linked_to_plan: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Filter products that are not linked to any plan
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
