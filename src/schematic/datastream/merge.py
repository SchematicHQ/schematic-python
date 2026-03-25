from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from ..types.rulesengine_company import RulesengineCompany
from ..types.rulesengine_company_metric import RulesengineCompanyMetric
from ..types.rulesengine_user import RulesengineUser


def extract_id(data: Any) -> Optional[str]:
    """Extract the 'id' field from a dict or Pydantic model."""
    if isinstance(data, dict):
        return data.get("id")
    return getattr(data, "id", None)


def partial_company(existing: RulesengineCompany, partial: Dict[str, Any]) -> RulesengineCompany:
    """Merge a partial update dict into an existing Company.

    Only fields present in `partial` are applied. Maps (keys, credit_balances)
    merge additively. Metrics are upserted by (event_subtype, period, month_reset).
    All other fields replace the existing value. The original is not mutated.
    """
    if "id" not in partial:
        raise ValueError("partial company message missing required field: id")

    updates: Dict[str, Any] = {}

    for key, value in partial.items():
        if key == "keys":
            merged_keys = dict(existing.keys) if existing.keys else {}
            merged_keys.update(value or {})
            updates["keys"] = merged_keys
        elif key == "credit_balances":
            merged_cb = dict(existing.credit_balances) if existing.credit_balances else {}
            merged_cb.update(value or {})
            updates["credit_balances"] = merged_cb
        elif key == "metrics":
            incoming = _parse_metrics(value)
            existing_metrics = [m.model_dump() for m in (existing.metrics or [])]
            updates["metrics"] = _upsert_metrics(existing_metrics, incoming)
        else:
            updates[key] = value

    base = existing.model_dump()
    base.update(updates)
    return RulesengineCompany.model_validate(base)


def partial_user(existing: RulesengineUser, partial: Dict[str, Any]) -> RulesengineUser:
    """Merge a partial update dict into an existing User.

    Only fields present in `partial` are applied. Keys map merges additively.
    All other fields replace the existing value. The original is not mutated.
    """
    if "id" not in partial:
        raise ValueError("partial user message missing required field: id")

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
