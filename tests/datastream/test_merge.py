from __future__ import annotations

import datetime as dt

import pytest

from schematic.datastream.merge import (
    deep_copy_company,
    deep_copy_user,
    extract_id,
    partial_company,
    partial_user,
)
from schematic.types import (
    RulesengineCompany,
    RulesengineCompanyMetric,
    RulesengineFeatureEntitlement,
    RulesengineRule,
    RulesengineSubscription,
    RulesengineTrait,
    RulesengineTraitDefinition,
    RulesengineUser,
)


def _make_trait(value: str, definition_id: str | None = None) -> RulesengineTrait:
    td = None
    if definition_id is not None:
        td = RulesengineTraitDefinition(
            id=definition_id,
            comparable_type="string",
            entity_type="company",
        )
    return RulesengineTrait(value=value, trait_definition=td)


def _make_rule(rule_id: str) -> RulesengineRule:
    return RulesengineRule(
        id=rule_id,
        name=rule_id,
        priority=1,
        value=True,
        rule_type="override",
        account_id="acc-1",
        environment_id="env-1",
        condition_groups=[],
        conditions=[],
    )


def _make_entitlement(feature_id: str, feature_key: str) -> RulesengineFeatureEntitlement:
    return RulesengineFeatureEntitlement(
        feature_id=feature_id,
        feature_key=feature_key,
        value_type="boolean",
    )


def _make_metric(
    event_subtype: str,
    period: str = "all_time",
    month_reset: str = "first_of_month",
    value: int = 0,
) -> RulesengineCompanyMetric:
    return RulesengineCompanyMetric(
        account_id="acc-1",
        company_id="co-1",
        created_at=dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc),
        environment_id="env-1",
        event_subtype=event_subtype,
        month_reset=month_reset,
        period=period,
        value=value,
    )


def base_company() -> RulesengineCompany:
    return RulesengineCompany(
        id="co-1",
        account_id="acc-1",
        environment_id="env-1",
        base_plan_id="plan-1",
        billing_product_ids=["bp-1"],
        credit_balances={"credit-1": 100.0},
        keys={"domain": "example.com"},
        plan_ids=["plan-1"],
        plan_version_ids=["pv-1"],
        traits=[_make_trait("Enterprise", "plan")],
        entitlements=[_make_entitlement("feat-1", "feature-one")],
        metrics=[],
        rules=[],
    )


def base_user() -> RulesengineUser:
    return RulesengineUser(
        id="user-1",
        account_id="acc-1",
        environment_id="env-1",
        keys={"email": "user@example.com"},
        traits=[_make_trait("Premium", "tier")],
        rules=[],
    )


# ------------------------------------------------------------------
# partial_company tests
# ------------------------------------------------------------------


class TestPartialCompanyOnlyTraits:
    def test_replaces_traits_preserves_other_fields(self) -> None:
        existing = base_company()
        partial = {
            "id": "co-1",
            "traits": [{"value": "Startup", "trait_definition": {"id": "plan", "comparable_type": "string", "entity_type": "company"}}],
        }

        merged = partial_company(existing, partial)

        assert len(merged.traits) == 1
        assert merged.traits[0].value == "Startup"

        assert merged.account_id == "acc-1"
        assert merged.environment_id == "env-1"
        assert merged.keys == {"domain": "example.com"}
        assert merged.billing_product_ids == ["bp-1"]
        assert merged.base_plan_id == "plan-1"


class TestPartialCompanyMergesKeys:
    def test_new_key_added_existing_preserved(self) -> None:
        existing = base_company()
        partial = {"id": "co-1", "keys": {"slug": "new-slug"}}

        merged = partial_company(existing, partial)

        assert merged.keys == {"domain": "example.com", "slug": "new-slug"}
        assert len(merged.traits) == 1


class TestPartialCompanyMergesCreditBalances:
    def test_new_balance_added_existing_preserved(self) -> None:
        existing = base_company()
        partial = {"id": "co-1", "credit_balances": {"credit-2": 200.0}}

        merged = partial_company(existing, partial)

        assert merged.credit_balances == {"credit-1": 100.0, "credit-2": 200.0}

    def test_overwrites_existing_balance(self) -> None:
        existing = base_company()
        partial = {"id": "co-1", "credit_balances": {"credit-1": 50.0}}

        merged = partial_company(existing, partial)

        assert merged.credit_balances == {"credit-1": 50.0}


class TestPartialCompanyUpsertsMetrics:
    def test_updates_matching_appends_new(self) -> None:
        existing = base_company().model_copy(
            update={
                "metrics": [
                    _make_metric("event-a", "all_time", "first_of_month", 10),
                    _make_metric("event-b", "current_month", "first_of_month", 5),
                ],
            }
        )
        partial = {
            "id": "co-1",
            "metrics": [
                {"event_subtype": "event-a", "period": "all_time", "month_reset": "first_of_month", "value": 42,
                 "account_id": "acc-1", "company_id": "co-1", "environment_id": "env-1",
                 "created_at": "2026-01-01T00:00:00Z"},
                {"event_subtype": "event-c", "period": "current_day", "month_reset": "billing_cycle", "value": 1,
                 "account_id": "acc-1", "company_id": "co-1", "environment_id": "env-1",
                 "created_at": "2026-01-01T00:00:00Z"},
            ],
        }

        merged = partial_company(existing, partial)

        assert len(merged.metrics) == 3
        # event-a updated in place
        assert merged.metrics[0].event_subtype == "event-a"
        assert merged.metrics[0].value == 42
        # event-b unchanged
        assert merged.metrics[1].event_subtype == "event-b"
        assert merged.metrics[1].value == 5
        # event-c appended
        assert merged.metrics[2].event_subtype == "event-c"
        assert merged.metrics[2].value == 1

        # Original not mutated
        assert existing.metrics[0].value == 10


class TestPartialCompanyEmptyEntitlements:
    def test_clears_entitlements(self) -> None:
        existing = base_company()
        partial = {"id": "co-1", "entitlements": []}

        merged = partial_company(existing, partial)

        assert merged.entitlements == []
        assert merged.account_id == "acc-1"


class TestPartialCompanyNullBasePlanID:
    def test_sets_base_plan_to_none(self) -> None:
        existing = base_company()
        partial = {"id": "co-1", "base_plan_id": None}

        merged = partial_company(existing, partial)

        assert merged.base_plan_id is None
        assert merged.billing_product_ids == ["bp-1"]


class TestPartialCompanyMissingID:
    def test_raises_value_error(self) -> None:
        existing = base_company()
        partial = {"traits": []}

        with pytest.raises(ValueError, match="missing required field: id"):
            partial_company(existing, partial)


class TestPartialCompanyDoesNotMutateOriginal:
    def test_original_unchanged(self) -> None:
        existing = base_company()
        orig_keys = dict(existing.keys)

        partial = {"id": "co-1", "keys": {"slug": "new-slug"}, "traits": []}

        merged = partial_company(existing, partial)

        assert existing.keys == orig_keys
        assert len(existing.traits) == 1
        assert merged.keys == {"domain": "example.com", "slug": "new-slug"}
        assert merged.traits == []


class TestPartialCompanyRules:
    def test_replaces_rules(self) -> None:
        existing = base_company().model_copy(update={"rules": [_make_rule("rule-old")]})
        partial = {
            "id": "co-1",
            "rules": [{"id": "rule-new", "name": "rule-new", "priority": 1, "value": True,
                        "rule_type": "override", "account_id": "acc-1", "environment_id": "env-1",
                        "condition_groups": [], "conditions": []}],
        }

        merged = partial_company(existing, partial)

        assert len(merged.rules) == 1
        assert merged.rules[0].id == "rule-new"
        assert existing.rules[0].id == "rule-old"


class TestPartialCompanyFullEntity:
    def test_full_entity_partial_message(self) -> None:
        existing = base_company().model_copy(
            update={
                "metrics": [_make_metric("event-a", "all_time", "first_of_month", 10)],
                "rules": [_make_rule("rule-1")],
            }
        )

        partial = {
            "id": "co-1",
            "account_id": "acc-2",
            "environment_id": "env-2",
            "base_plan_id": "plan-99",
            "billing_product_ids": ["bp-10", "bp-20"],
            "credit_balances": {"credit-1": 999.0, "credit-new": 50.0},
            "entitlements": [
                {"feature_id": "feat-new", "feature_key": "feature-new", "value_type": "boolean"},
                {"feature_id": "feat-2", "feature_key": "feature-two", "value_type": "boolean"},
            ],
            "keys": {"domain": "new.com", "slug": "new-slug"},
            "metrics": [
                {"event_subtype": "event-a", "period": "all_time", "month_reset": "first_of_month", "value": 42,
                 "account_id": "acc-1", "company_id": "co-1", "environment_id": "env-1",
                 "created_at": "2026-01-01T00:00:00Z"},
                {"event_subtype": "event-new", "period": "current_day", "month_reset": "billing_cycle", "value": 7,
                 "account_id": "acc-1", "company_id": "co-1", "environment_id": "env-1",
                 "created_at": "2026-01-01T00:00:00Z"},
            ],
            "plan_ids": ["plan-99", "plan-100"],
            "plan_version_ids": ["pv-99"],
            "rules": [
                {"id": "rule-new-1", "name": "r1", "priority": 1, "value": True, "rule_type": "override",
                 "account_id": "acc-1", "environment_id": "env-1", "condition_groups": [], "conditions": []},
                {"id": "rule-new-2", "name": "r2", "priority": 2, "value": False, "rule_type": "override",
                 "account_id": "acc-1", "environment_id": "env-1", "condition_groups": [], "conditions": []},
            ],
            "subscription": {"id": "sub-new", "period_start": "2026-01-01T00:00:00Z", "period_end": "2026-02-01T00:00:00Z"},
            "traits": [
                {"value": "Startup", "trait_definition": {"id": "tier", "comparable_type": "string", "entity_type": "company"}},
                {"value": "Annual", "trait_definition": {"id": "billing", "comparable_type": "string", "entity_type": "company"}},
            ],
        }

        merged = partial_company(existing, partial)

        assert merged.id == "co-1"
        assert merged.account_id == "acc-2"
        assert merged.environment_id == "env-2"
        assert merged.base_plan_id == "plan-99"
        assert merged.billing_product_ids == ["bp-10", "bp-20"]

        # Credit balances merge: existing credit-1 overwritten, credit-new added
        assert merged.credit_balances == {"credit-1": 999.0, "credit-new": 50.0}

        assert len(merged.entitlements) == 2
        assert merged.entitlements[0].feature_id == "feat-new"
        assert merged.entitlements[1].feature_id == "feat-2"

        # Keys merge: domain overwritten, slug added
        assert merged.keys == {"domain": "new.com", "slug": "new-slug"}

        # Metrics upsert: event-a updated, event-new appended
        assert len(merged.metrics) == 2
        assert merged.metrics[0].event_subtype == "event-a"
        assert merged.metrics[0].value == 42
        assert merged.metrics[1].event_subtype == "event-new"
        assert merged.metrics[1].value == 7

        assert merged.plan_ids == ["plan-99", "plan-100"]
        assert merged.plan_version_ids == ["pv-99"]

        assert len(merged.rules) == 2
        assert merged.rules[0].id == "rule-new-1"
        assert merged.rules[1].id == "rule-new-2"

        assert merged.subscription is not None
        assert merged.subscription.id == "sub-new"

        assert len(merged.traits) == 2
        assert merged.traits[0].value == "Startup"
        assert merged.traits[1].value == "Annual"

        # Original not mutated
        assert existing.account_id == "acc-1"
        assert existing.base_plan_id == "plan-1"
        assert existing.keys == {"domain": "example.com"}
        assert existing.metrics[0].value == 10


# ------------------------------------------------------------------
# partial_user tests
# ------------------------------------------------------------------


class TestPartialUserOnlyTraits:
    def test_replaces_traits_preserves_keys(self) -> None:
        existing = base_user()
        partial = {
            "id": "user-1",
            "traits": [{"value": "Free", "trait_definition": {"id": "tier", "comparable_type": "string", "entity_type": "user"}}],
        }

        merged = partial_user(existing, partial)

        assert len(merged.traits) == 1
        assert merged.traits[0].value == "Free"
        assert merged.keys == {"email": "user@example.com"}


class TestPartialUserMergesKeys:
    def test_new_key_added_existing_preserved(self) -> None:
        existing = base_user()
        partial = {"id": "user-1", "keys": {"slack_id": "U123"}}

        merged = partial_user(existing, partial)

        assert merged.keys == {"email": "user@example.com", "slack_id": "U123"}
        assert len(merged.traits) == 1


class TestPartialUserMissingID:
    def test_raises_value_error(self) -> None:
        existing = base_user()
        partial = {"keys": {"email": "new@example.com"}}

        with pytest.raises(ValueError, match="missing required field: id"):
            partial_user(existing, partial)


class TestPartialUserDoesNotMutateOriginal:
    def test_original_unchanged(self) -> None:
        existing = base_user()
        orig_keys = dict(existing.keys)

        partial = {"id": "user-1", "keys": {"slug": "new"}, "traits": []}

        merged = partial_user(existing, partial)

        assert existing.keys == orig_keys
        assert len(existing.traits) == 1
        assert merged.keys == {"email": "user@example.com", "slug": "new"}
        assert merged.traits == []


class TestPartialUserFullEntity:
    def test_full_entity_partial_message(self) -> None:
        existing = base_user().model_copy(update={"rules": [_make_rule("rule-1")]})

        partial = {
            "id": "user-1",
            "account_id": "acc-2",
            "environment_id": "env-2",
            "keys": {"email": "new@example.com", "slack_id": "U999"},
            "traits": [
                {"value": "Free", "trait_definition": {"id": "tier", "comparable_type": "string", "entity_type": "user"}},
                {"value": "Monthly", "trait_definition": {"id": "billing", "comparable_type": "string", "entity_type": "user"}},
            ],
            "rules": [
                {"id": "rule-new-1", "name": "r1", "priority": 1, "value": True, "rule_type": "override",
                 "account_id": "acc-1", "environment_id": "env-1", "condition_groups": [], "conditions": []},
                {"id": "rule-new-2", "name": "r2", "priority": 2, "value": False, "rule_type": "override",
                 "account_id": "acc-1", "environment_id": "env-1", "condition_groups": [], "conditions": []},
            ],
        }

        merged = partial_user(existing, partial)

        assert merged.id == "user-1"
        assert merged.account_id == "acc-2"
        assert merged.environment_id == "env-2"

        # Keys merge: email overwritten, slack_id added
        assert merged.keys == {"email": "new@example.com", "slack_id": "U999"}

        assert len(merged.traits) == 2
        assert merged.traits[0].value == "Free"
        assert merged.traits[1].value == "Monthly"

        assert len(merged.rules) == 2
        assert merged.rules[0].id == "rule-new-1"
        assert merged.rules[1].id == "rule-new-2"

        # Original not mutated
        assert existing.account_id == "acc-1"
        assert existing.keys == {"email": "user@example.com"}
        assert len(existing.traits) == 1
        assert existing.rules[0].id == "rule-1"


# ------------------------------------------------------------------
# extract_id tests
# ------------------------------------------------------------------


class TestExtractID:
    def test_from_dict(self) -> None:
        assert extract_id({"id": "co-1", "traits": []}) == "co-1"

    def test_from_model(self) -> None:
        user = base_user()
        assert extract_id(user) == "user-1"

    def test_missing_returns_none(self) -> None:
        assert extract_id({"traits": []}) is None

    def test_none_returns_none(self) -> None:
        assert extract_id(None) is None


# ------------------------------------------------------------------
# deep_copy tests
# ------------------------------------------------------------------


class TestDeepCopyCompany:
    def test_none_returns_none(self) -> None:
        assert deep_copy_company(None) is None

    def test_full_copy_is_independent(self) -> None:
        orig = base_company().model_copy(
            update={
                "subscription": RulesengineSubscription(
                    id="sub-1",
                    period_start=dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc),
                    period_end=dt.datetime(2026, 2, 1, tzinfo=dt.timezone.utc),
                ),
                "metrics": [
                    _make_metric("event-1", value=42),
                ],
            }
        )

        cp = deep_copy_company(orig)

        assert cp.id == orig.id
        assert cp.account_id == orig.account_id
        assert cp.environment_id == orig.environment_id
        assert cp.base_plan_id == orig.base_plan_id
        assert cp.keys == orig.keys
        assert cp.credit_balances == orig.credit_balances
        assert cp.subscription.id == "sub-1"
        assert cp.metrics[0].value == 42

        # Verify it's a separate object
        assert cp is not orig


class TestDeepCopyUser:
    def test_empty_fields(self) -> None:
        orig = RulesengineUser(
            id="u1",
            account_id="acc-1",
            environment_id="env-1",
            keys={},
            traits=[],
            rules=[],
        )
        cp = deep_copy_user(orig)

        assert cp.id == "u1"
        assert cp.keys == {}
        assert cp.traits == []
        assert cp.rules == []

    def test_full_copy_is_independent(self) -> None:
        orig = base_user().model_copy(update={"rules": [_make_rule("r1")]})

        cp = deep_copy_user(orig)

        assert cp.id == orig.id
        assert cp.account_id == orig.account_id
        assert cp.keys == orig.keys
        assert cp.traits[0].value == "Premium"
        assert cp.rules[0].id == "r1"

        # Verify it's a separate object
        assert cp is not orig

    def test_none_returns_none(self) -> None:
        assert deep_copy_user(None) is None
