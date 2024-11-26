# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class CountCompanyOverridesParams(UniversalBaseModel):
    """
    Input parameters
    """

    company_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Filter company overrides by a single company ID (starting with comp\_)
    """

    company_ids: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    Filter company overrides by multiple company IDs (starting with comp\_)
    """

    feature_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Filter company overrides by a single feature ID (starting with feat\_)
    """

    feature_ids: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    Filter company overrides by multiple feature IDs (starting with feat\_)
    """

    ids: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    Filter company overrides by multiple company override IDs (starting with cmov\_)
    """

    limit: typing.Optional[int] = pydantic.Field(default=None)
    """
    Page limit (default 100)
    """

    offset: typing.Optional[int] = pydantic.Field(default=None)
    """
    Page offset (default 0)
    """

    q: typing.Optional[str] = pydantic.Field(default=None)
    """
    Search for company overrides by feature or company name
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
