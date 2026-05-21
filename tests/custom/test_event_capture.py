"""Tests for the event capture wire-format mapping.

The capture service expects a specific JSON shape (api_key + type + optional
metadata) that's different from the Fern-generated CreateEventRequestBody.
These tests pin the mapping so optional fields like idempotency_key don't
silently get dropped on the way to the wire.
"""
from __future__ import annotations

import datetime as dt
import json

from schematic.event_capture import (
    _CaptureBatchPayload,
    _CaptureEventPayload,
    _serialize_batch,
    _to_payload,
)
from schematic.types import CreateEventRequestBody, EventBodyTrack


def _make_event(**overrides) -> CreateEventRequestBody:
    """Build a track event with arbitrary CreateEventRequestBody overrides."""
    return CreateEventRequestBody(
        event_type="track",
        body=EventBodyTrack(
            event="some-event",
            company={"id": "co_123"},
        ),
        **overrides,
    )


class TestToPayloadMapping:
    """_to_payload must copy every optional metadata field from
    CreateEventRequestBody onto _CaptureEventPayload, so the capture service
    receives values the SDK consumer set."""

    def test_minimum_required_fields(self) -> None:
        event = _make_event()
        payload = _to_payload(event, api_key="sch_test")

        assert payload.api_key == "sch_test"
        assert payload.type == "track"
        assert payload.body is not None
        assert payload.idempotency_key is None
        assert payload.sent_at is None
        assert payload.trusted_client_clock is None
        assert payload.backfill is None

    def test_idempotency_key_mapped(self) -> None:
        event = _make_event(idempotency_key="evt_abc123")
        payload = _to_payload(event, api_key="sch_test")
        assert payload.idempotency_key == "evt_abc123"

    def test_sent_at_mapped(self) -> None:
        sent = dt.datetime(2026, 5, 21, 12, 0, 0, tzinfo=dt.timezone.utc)
        event = _make_event(sent_at=sent)
        payload = _to_payload(event, api_key="sch_test")
        assert payload.sent_at == sent

    def test_trusted_client_clock_mapped(self) -> None:
        event = _make_event(trusted_client_clock=True)
        payload = _to_payload(event, api_key="sch_test")
        assert payload.trusted_client_clock is True

    def test_backfill_mapped(self) -> None:
        event = _make_event(backfill=True)
        payload = _to_payload(event, api_key="sch_test")
        assert payload.backfill is True

    def test_all_optional_fields_mapped_together(self) -> None:
        sent = dt.datetime(2026, 5, 21, 12, 0, 0, tzinfo=dt.timezone.utc)
        event = _make_event(
            idempotency_key="evt_xyz",
            sent_at=sent,
            trusted_client_clock=True,
            backfill=True,
        )
        payload = _to_payload(event, api_key="sch_test")
        assert payload.idempotency_key == "evt_xyz"
        assert payload.sent_at == sent
        assert payload.trusted_client_clock is True
        assert payload.backfill is True


class TestSerializeBatch:
    """The serialized JSON sent to the capture service must include the
    optional metadata fields when set, and must exclude them (rather than
    sending explicit nulls) when unset."""

    def test_unset_optional_fields_excluded_from_wire(self) -> None:
        event = _make_event()
        body = _serialize_batch([event], api_key="sch_test")
        data = json.loads(body)

        wire_event = data["events"][0]
        assert wire_event["api_key"] == "sch_test"
        assert wire_event["type"] == "track"
        # Unset fields should not appear at all — exclude_none on the model
        # ensures we don't send `"idempotency_key": null` and friends.
        assert "idempotency_key" not in wire_event
        assert "sent_at" not in wire_event
        assert "trusted_client_clock" not in wire_event
        assert "backfill" not in wire_event

    def test_set_optional_fields_appear_on_wire(self) -> None:
        sent = dt.datetime(2026, 5, 21, 12, 0, 0, tzinfo=dt.timezone.utc)
        event = _make_event(
            idempotency_key="evt_xyz",
            sent_at=sent,
            trusted_client_clock=True,
            backfill=False,
        )
        body = _serialize_batch([event], api_key="sch_test")
        data = json.loads(body)

        wire_event = data["events"][0]
        assert wire_event["idempotency_key"] == "evt_xyz"
        assert wire_event["trusted_client_clock"] is True
        # backfill=False is explicitly set, so it must reach the wire even
        # though the value is falsy.
        assert wire_event["backfill"] is False
        assert "sent_at" in wire_event


class TestCapturePayloadShape:
    """Pin the wire field names so the capture service contract doesn't
    silently drift if someone renames a Pydantic field."""

    def test_uses_type_not_event_type(self) -> None:
        """The capture service expects `type` (matching Go/Ruby/C# SDKs),
        not `event_type` (which is the REST API name)."""
        payload = _CaptureEventPayload(api_key="k", type="track")
        dumped = payload.model_dump()
        assert "type" in dumped
        assert "event_type" not in dumped

    def test_batch_wrapper_uses_events_field(self) -> None:
        batch = _CaptureBatchPayload(events=[])
        dumped = batch.model_dump()
        assert "events" in dumped
        assert dumped["events"] == []
