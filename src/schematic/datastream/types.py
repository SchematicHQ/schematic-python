from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any, Dict, Optional


class EntityType(str, enum.Enum):
    COMPANY = "rulesengine.Company"
    USER = "rulesengine.User"
    FLAG = "rulesengine.Flag"
    FLAGS = "rulesengine.Flags"


class MessageType(str, enum.Enum):
    FULL = "full"
    PARTIAL = "partial"
    DELETE = "delete"
    ERROR = "error"
    UNKNOWN = "unknown"


class Action(str, enum.Enum):
    START = "start"
    STOP = "stop"


@dataclass
class DataStreamReq:
    """Request message sent to the datastream."""

    entity_type: EntityType
    keys: Optional[Dict[str, str]] = None
    action: Action = Action.START

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "action": self.action.value,
            "entity_type": self.entity_type.value,
        }
        if self.keys is not None:
            d["keys"] = self.keys
        return d


@dataclass
class DataStreamBaseReq:
    """Wrapper around DataStreamReq — the wire format expected by the server."""

    data: DataStreamReq

    def to_dict(self) -> Dict[str, Any]:
        return {"data": self.data.to_dict()}


@dataclass
class DataStreamResp:
    """Response message received from the datastream."""

    data: Any
    entity_type: str
    message_type: str
    entity_id: Optional[str] = None


@dataclass
class DataStreamError:
    """Error message received from the datastream."""

    error: str
    keys: Optional[Dict[str, str]] = None
    entity_type: Optional[EntityType] = None


class KeyConflictError(Exception):
    """Raised when lookup keys resolve to multiple distinct entities."""
