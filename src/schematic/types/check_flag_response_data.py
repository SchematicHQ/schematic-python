# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class CheckFlagResponseData(UniversalBaseModel):
    """
    The returned resource
    """

    company_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    If company keys were provided and matched a company, its ID
    """

    error: typing.Optional[str] = pydantic.Field(default=None)
    """
    If an error occurred while checking the flag, the error message
    """

    feature_allocation: typing.Optional[int] = pydantic.Field(default=None)
    """
    If a numeric feature entitlement rule was matched, its allocation
    """

    feature_usage: typing.Optional[int] = pydantic.Field(default=None)
    """
    If a numeric feature entitlement rule was matched, the company's usage
    """

    feature_usage_event: typing.Optional[str] = pydantic.Field(default=None)
    """
    If an event-based numeric feature entitlement rule was matched, the event used to track its usage
    """

    feature_usage_period: typing.Optional[str] = pydantic.Field(default=None)
    """
    For event-based feature entitlement rules, the period over which usage is tracked (current_month, current_day, current_week, all_time)
    """

    feature_usage_reset_at: typing.Optional[dt.datetime] = pydantic.Field(default=None)
    """
    For event-based feature entitlement rules, when the usage period will reset
    """

    flag: str = pydantic.Field()
    """
    The key used to check the flag
    """

    flag_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    If a flag was found, its ID
    """

    reason: str = pydantic.Field()
    """
    A human-readable explanation of the result
    """

    rule_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    If a rule was found, its ID
    """

    rule_type: typing.Optional[str] = pydantic.Field(default=None)
    """
    If a rule was found, its type
    """

    user_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    If user keys were provided and matched a user, its ID
    """

    value: bool = pydantic.Field()
    """
    A boolean flag check result; for feature entitlements, this represents whether further consumption of the feature is permitted
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
