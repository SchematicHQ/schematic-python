# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ListPlanEntitlementsParams(UniversalBaseModel):
    """
    Input parameters
    """

    feature_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Filter plan entitlements by a single feature ID (starting with feat\_)
    """

    feature_ids: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    Filter plan entitlements by multiple feature IDs (starting with feat\_)
    """

    ids: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    Filter plan entitlements by multiple plan entitlement IDs (starting with pltl\_)
    """

    limit: typing.Optional[int] = pydantic.Field(default=None)
    """
    Page limit (default 100)
    """

    offset: typing.Optional[int] = pydantic.Field(default=None)
    """
    Page offset (default 0)
    """

    plan_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Filter plan entitlements by a single plan ID (starting with plan\_)
    """

    plan_ids: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    Filter plan entitlements by multiple plan IDs (starting with plan\_)
    """

    q: typing.Optional[str] = pydantic.Field(default=None)
    """
    Search for plan entitlements by feature or company name
    """

    with_metered_products: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Filter plan entitlements only with metered products
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
