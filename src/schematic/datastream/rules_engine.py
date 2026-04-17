from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Optional

from ..types.rulesengine_check_flag_result import RulesengineCheckFlagResult
from ..types.rulesengine_company import RulesengineCompany
from ..types.rulesengine_flag import RulesengineFlag
from ..types.rulesengine_user import RulesengineUser

logger = logging.getLogger(__name__)

_CAMEL_RE = re.compile(r"([A-Z])")


def _camel_to_snake(name: str) -> str:
    """Convert a camelCase string to snake_case."""
    return _CAMEL_RE.sub(r"_\1", name).lower().lstrip("_")


def _deep_camel_to_snake(obj: Any) -> Any:
    """Recursively convert all dict keys from camelCase to snake_case."""
    if isinstance(obj, dict):
        return {_camel_to_snake(k): _deep_camel_to_snake(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_deep_camel_to_snake(item) for item in obj]
    return obj

# Path to the WASM binary shipped alongside this module
_WASM_PATH = Path(__file__).parent / "wasm" / "rulesengine.wasm"


class RulesEngineClient:
    """Wrapper around the Rust WASM rules engine for local flag evaluation.

    Uses ``wasmtime`` to load and execute the raw WASM binary.  The WASM
    module exposes a ``checkFlagCombined`` function that accepts a single
    JSON envelope ``{"flag": ..., "company": ..., "user": ...}`` and returns
    the evaluation result.  All WASM memory management is handled internally
    via the module's ``alloc``/``dealloc`` exports.

    Usage::

        engine = RulesEngineClient()
        await engine.initialize()
        result = engine.check_flag(flag, company, user)
    """

    def __init__(self, *, wasm_path: Optional[str] = None) -> None:
        self._wasm_path = Path(wasm_path) if wasm_path else _WASM_PATH
        self._initialized = False
        # wasmtime objects — set during initialize()
        self._store: Any = None
        self._instance: Any = None
        self._memory: Any = None
        self._alloc_fn: Any = None
        self._dealloc_fn: Any = None
        self._check_flag_fn: Any = None
        self._get_result_json_fn: Any = None
        self._get_result_json_length_fn: Any = None
        self._get_version_key_fn: Any = None
        self._version_key: Optional[str] = None

    async def initialize(self) -> None:
        """Load and instantiate the WASM module. Safe to call multiple times."""
        if self._initialized:
            return

        try:
            import wasmtime  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "wasmtime is required for the rules engine. "
                "Install it with: pip install 'schematichq[datastream]' or pip install wasmtime"
            )

        if not self._wasm_path.exists():
            raise FileNotFoundError(
                f"WASM binary not found at {self._wasm_path}. "
                "Ensure the rules engine WASM has been deployed to this SDK."
            )

        engine = wasmtime.Engine()
        module = wasmtime.Module.from_file(engine, str(self._wasm_path))
        linker = wasmtime.Linker(engine)
        linker.define_wasi()

        wasi_config = wasmtime.WasiConfig()
        self._store = wasmtime.Store(engine)
        self._store.set_wasi(wasi_config)

        self._instance = linker.instantiate(self._store, module)
        exports = self._instance.exports(self._store)

        self._memory = exports.get("memory")
        self._alloc_fn = exports.get("alloc")
        self._dealloc_fn = exports.get("dealloc")
        self._check_flag_fn = exports.get("checkFlagCombined")
        self._get_result_json_fn = exports.get("getResultJson")
        self._get_result_json_length_fn = exports.get("getResultJsonLength")
        self._get_version_key_fn = exports.get("get_version_key_wasm")

        if self._memory is None:
            raise RuntimeError("WASM module does not export 'memory'")
        if self._alloc_fn is None:
            raise RuntimeError("WASM module does not export 'alloc'")
        if self._check_flag_fn is None:
            raise RuntimeError("WASM module does not export 'checkFlagCombined'")

        self._initialized = True
        # Cache the version key immediately — the WASM pointer is only stable
        # before any other WASM calls mutate the linear memory.
        self._version_key = self._read_version_key_from_wasm()
        logger.debug("Rules engine WASM initialized (version: %s)", self._version_key)

    def is_initialized(self) -> bool:
        return self._initialized

    def check_flag(
        self,
        flag: RulesengineFlag,
        company: Optional[RulesengineCompany] = None,
        user: Optional[RulesengineUser] = None,
    ) -> RulesengineCheckFlagResult:
        """Evaluate a flag using the WASM rules engine.

        Accepts Fern-generated Pydantic models (or plain dicts).  Serialises
        them into a single JSON envelope, passes it to the WASM module, and
        returns a ``RulesengineCheckFlagResult``.
        """
        self._ensure_initialized()

        envelope = {
            "flag": flag.model_dump(exclude_none=True, mode="json"),
            "company": company.model_dump(exclude_none=True, mode="json") if company else None,
            "user": user.model_dump(exclude_none=True, mode="json") if user else None,
        }

        result_json = self._call_wasm(json.dumps(envelope))
        result_data = _deep_camel_to_snake(json.loads(result_json))
        return RulesengineCheckFlagResult(**result_data)

    def get_version_key(self) -> str:
        """Get the version key from the WASM rules engine.

        Used for cache key generation to ensure cache invalidation on engine updates.
        The value is computed once during initialization and cached.
        """
        self._ensure_initialized()
        return self._version_key or "1"

    def _read_version_key_from_wasm(self) -> str:
        """Read the version key from WASM. Called once during init."""
        if self._get_version_key_fn is None:
            return "1"
        ptr = self._get_version_key_fn(self._store)
        return self._read_null_terminated_string(ptr)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_initialized(self) -> None:
        if not self._initialized:
            raise RuntimeError("Rules engine not initialized. Call initialize() first.")

    def _call_wasm(self, input_json: str) -> str:
        """Write *input_json* into WASM memory, invoke the engine, and return
        the result JSON string.  All memory is allocated/freed via the WASM
        module's own ``alloc``/``dealloc`` exports."""

        data = input_json.encode("utf-8")
        length = len(data)

        # Allocate a buffer inside WASM memory and copy our JSON into it
        ptr = self._alloc_fn(self._store, length)
        try:
            self._memory.write(self._store, data, ptr)

            result_len = self._check_flag_fn(self._store, ptr, length)
            if result_len < 0:
                raise RuntimeError("WASM checkFlagCombined returned error code")
        finally:
            self._dealloc_fn(self._store, ptr, length)

        # Read the result (owned by WASM thread-local, no need to free)
        result_ptr = self._get_result_json_fn(self._store)
        actual_len = self._get_result_json_length_fn(self._store)
        return bytes(self._memory.read(self._store, result_ptr, result_ptr + actual_len)).decode("utf-8")

    def _read_null_terminated_string(self, ptr: int, max_length: int = 256) -> str:
        """Read a null-terminated UTF-8 string from WASM linear memory."""
        raw = self._memory.read(self._store, ptr, ptr + max_length)
        null_idx = raw.find(0)
        if null_idx >= 0:
            raw = raw[:null_idx]
        return raw.decode("utf-8").strip()
