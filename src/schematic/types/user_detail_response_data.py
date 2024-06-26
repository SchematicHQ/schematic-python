# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .company_membership_detail_response_data import CompanyMembershipDetailResponseData
from .entity_key_detail_response_data import EntityKeyDetailResponseData
from .entity_trait_detail_response_data import EntityTraitDetailResponseData


class UserDetailResponseData(pydantic_v1.BaseModel):
    company_memberships: typing.List[CompanyMembershipDetailResponseData]
    created_at: dt.datetime
    entity_traits: typing.List[EntityTraitDetailResponseData]
    environment_id: str
    id: str
    keys: typing.List[EntityKeyDetailResponseData]
    last_seen_at: typing.Optional[dt.datetime] = None
    name: str
    traits: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(default=None)
    """
    A map of trait names to trait values
    """

    updated_at: dt.datetime

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
