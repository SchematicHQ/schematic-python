from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from ..types.rulesengine_company import RulesengineCompany
from ..types.rulesengine_user import RulesengineUser


def partial_company(existing: RulesengineCompany, partial: Dict[str, Any]) -> RulesengineCompany:
    """Merge a partial update dict into an existing Company.

    Only fields present in `partial` are applied. Maps (keys, credit_balances)
    merge additively. Metrics are upserted by (event_subtype, period, month_reset).
    All other fields replace the existing value. The original is not mutated.

    Partials don't carry refreshed entitlements, so when their derived fields
    change in another part of the company we sync them here to match server
    behavior:
      - credit_remaining ← credit_balances[credit_id]
      - usage ← metric value matching (event_name, metric_period, month_reset)
    Both are skipped when the partial also sends entitlements wholesale.
    """
    updates: Dict[str, Any] = {}
    updated_balances: Optional[Dict[str, float]] = None
    metrics_updated = False

    for key, value in partial.items():
        if key == "keys":
            merged_keys = dict(existing.keys) if existing.keys else {}
            merged_keys.update(value or {})
            updates["keys"] = merged_keys
        elif key == "credit_balances":
            merged_cb = dict(existing.credit_balances) if existing.credit_balances else {}
            merged_cb.update(value or {})
            updates["credit_balances"] = merged_cb
            updated_balances = value or {}
        elif key == "metrics":
            incoming = _parse_metrics(value)
            existing_metrics = [m.model_dump() for m in (existing.metrics or [])]
            updates["metrics"] = _upsert_metrics(existing_metrics, incoming)
            metrics_updated = True
        else:
            updates[key] = value

    if (updated_balances or metrics_updated) and "entitlements" not in updates:
        existing_ents = existing.entitlements or []
        if existing_ents:
            metrics_lookup: Dict[Tuple[str, str, str], int] = {}
            if metrics_updated:
                for m in updates["metrics"]:
                    if isinstance(m, dict):
                        metrics_lookup[(
                            m.get("event_subtype", ""),
                            m.get("period", "") or "",
                            m.get("month_reset", "") or "",
                        )] = m.get("value", 0)

            new_ents = []
            for ent in existing_ents:
                ent_dict = ent.model_dump()
                if updated_balances and ent.credit_id and ent.credit_id in updated_balances:
                    ent_dict["credit_remaining"] = updated_balances[ent.credit_id]
                if metrics_lookup and ent.event_name:
                    period = ent.metric_period or "all_time"
                    month_reset = ent.month_reset or "first_of_month"
                    matched = metrics_lookup.get((ent.event_name, period, month_reset))
                    if matched is not None:
                        ent_dict["usage"] = matched
                new_ents.append(ent_dict)
            updates["entitlements"] = new_ents

    base = existing.model_dump()
    base.update(updates)
    return RulesengineCompany.model_validate(base)


def partial_user(existing: RulesengineUser, partial: Dict[str, Any]) -> RulesengineUser:
    """Merge a partial update dict into an existing User.

    Only fields present in `partial` are applied. Keys map merges additively.
    All other fields replace the existing value. The original is not mutated.
    """
    updates: Dict[str, Any] = {}

    for key, value in partial.items():
        if key == "keys":
            merged_keys = dict(existing.keys) if existing.keys else {}
            merged_keys.update(value or {})
            updates["keys"] = merged_keys
        else:
            updates[key] = value

    base = existing.model_dump()
    base.update(updates)
    return RulesengineUser.model_validate(base)


def deep_copy_company(company: Optional[RulesengineCompany]) -> Optional[RulesengineCompany]:
    """Create a deep copy of a Company. Returns None if input is None."""
    if company is None:
        return None
    return company.model_copy(deep=True)


def deep_copy_user(user: Optional[RulesengineUser]) -> Optional[RulesengineUser]:
    """Create a deep copy of a User. Returns None if input is None."""
    if user is None:
        return None
    return user.model_copy(deep=True)


def _metric_key(metric: Any) -> Tuple[str, str, str]:
    """Build the composite key used for metric upsert matching."""
    if isinstance(metric, dict):
        return (
            metric.get("event_subtype", ""),
            metric.get("period", ""),
            metric.get("month_reset", ""),
        )
    return (
        getattr(metric, "event_subtype", ""),
        str(getattr(metric, "period", "")),
        str(getattr(metric, "month_reset", "")),
    )


def _parse_metrics(raw: Any) -> List[Any]:
    """Normalise incoming metrics to a list."""
    if raw is None:
        return []
    if isinstance(raw, list):
        return raw
    return [raw]


def _upsert_metrics(existing: List[Any], incoming: List[Any]) -> List[Any]:
    """Merge incoming metrics into existing ones.

    Metrics are matched by (event_subtype, period, month_reset).
    Matches are replaced in place; new metrics are appended.
    """
    result = list(existing)
    index: Dict[Tuple[str, str, str], int] = {}
    for i, m in enumerate(result):
        if m is not None:
            index[_metric_key(m)] = i

    for m in incoming:
        if m is None:
            continue
        k = _metric_key(m)
        if k in index:
            result[index[k]] = m
        else:
            result.append(m)

    return result
