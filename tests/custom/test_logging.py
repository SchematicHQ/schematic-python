from __future__ import annotations

import logging
import uuid

from schematic.client import AsyncSchematic, AsyncSchematicConfig, Schematic, SchematicConfig
from schematic.logging import DEFAULT_LOG_LEVEL, get_default_logger


def _unique(name: str) -> str:
    """Use unique names so Python's global logger cache doesn't bleed state across tests."""
    return f"{name}-{uuid.uuid4().hex[:8]}"


class TestDefaultLogLevel:
    def test_default_level_is_warning(self) -> None:
        """Default must be WARNING — debug/info output is opt-in, not on by default."""
        assert DEFAULT_LOG_LEVEL == logging.WARNING

    def test_default_logger_uses_warning_when_no_level_specified(self) -> None:
        logger = get_default_logger(_unique("schematic-test"))
        assert logger.level == logging.WARNING

    def test_default_logger_drops_info_and_debug(self) -> None:
        """isEnabledFor is the canonical "would this level emit?" check.
        caplog can't be used here since pytest forcibly raises the level."""
        logger = get_default_logger(_unique("schematic-test"))
        assert not logger.isEnabledFor(logging.DEBUG)
        assert not logger.isEnabledFor(logging.INFO)
        assert logger.isEnabledFor(logging.WARNING)
        assert logger.isEnabledFor(logging.ERROR)


class TestConfigurableLevel:
    def test_explicit_level_is_applied(self) -> None:
        logger = get_default_logger(_unique("schematic-test"), level=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_handler_level_matches_logger_level(self) -> None:
        """The StreamHandler must also get the configured level — otherwise the
        logger lets the message through but the handler still suppresses it."""
        logger = get_default_logger(_unique("schematic-test"), level=logging.ERROR)
        assert len(logger.handlers) >= 1
        for handler in logger.handlers:
            assert handler.level == logging.ERROR

    def test_string_level_is_accepted(self) -> None:
        """Python's logging module accepts string levels; we shouldn't reject them."""
        logger = get_default_logger(_unique("schematic-test"), level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_re_call_updates_handler_level(self) -> None:
        """Python's getLogger() returns the same Logger instance for a given name,
        so a second call with a different level must keep the handler in sync —
        otherwise the first call's handler level wins forever."""
        name = _unique("schematic-test")
        logger = get_default_logger(name, level=logging.ERROR)
        for handler in logger.handlers:
            assert handler.level == logging.ERROR

        logger = get_default_logger(name, level=logging.DEBUG)
        assert logger.level == logging.DEBUG
        for handler in logger.handlers:
            assert handler.level == logging.DEBUG

    def test_does_not_mutate_foreign_handlers(self) -> None:
        """If a consumer has attached their own handlers to a same-named logger
        out-of-band, the SDK must only touch its own tagged handler."""
        name = _unique("schematic-test")
        logger = logging.getLogger(name)
        foreign = logging.StreamHandler()
        foreign.name = "consumer-handler"
        foreign.setLevel(logging.CRITICAL)
        logger.addHandler(foreign)

        get_default_logger(name, level=logging.DEBUG)

        # Foreign handler's level must be untouched.
        assert foreign.level == logging.CRITICAL
        # And the SDK's own handler is present and at the requested level.
        sdk_handlers = [h for h in logger.handlers if getattr(h, "name", None) == "schematichq-default"]
        assert len(sdk_handlers) == 1
        assert sdk_handlers[0].level == logging.DEBUG

    def test_re_call_does_not_add_duplicate_sdk_handler(self) -> None:
        """Calling get_default_logger twice with the same name should not stack
        SDK handlers — otherwise each call doubles the output."""
        name = _unique("schematic-test")
        get_default_logger(name, level=logging.WARNING)
        get_default_logger(name, level=logging.DEBUG)

        logger = logging.getLogger(name)
        sdk_handlers = [h for h in logger.handlers if getattr(h, "name", None) == "schematichq-default"]
        assert len(sdk_handlers) == 1


class TestSchematicConfigLogLevel:
    def test_sync_client_applies_log_level_to_default_logger(self) -> None:
        client = Schematic("test-key", config=SchematicConfig(
            offline=True, log_level=logging.DEBUG,
        ))
        assert client.logger.level == logging.DEBUG

    async def test_async_client_applies_log_level_to_default_logger(self) -> None:
        client = AsyncSchematic("test-key", config=AsyncSchematicConfig(
            offline=True, log_level=logging.DEBUG,
        ))
        try:
            assert client.logger.level == logging.DEBUG
        finally:
            await client.shutdown()

    def test_sync_client_default_is_warning(self) -> None:
        client = Schematic("test-key", config=SchematicConfig(offline=True))
        assert client.logger.level == logging.WARNING

    async def test_async_client_default_is_warning(self) -> None:
        client = AsyncSchematic("test-key", config=AsyncSchematicConfig(offline=True))
        try:
            assert client.logger.level == logging.WARNING
        finally:
            await client.shutdown()


class TestCustomLoggerRespectsItsOwnLevel:
    """When a consumer provides their own logger, the SDK must not touch its
    level — even if log_level is also set on the config."""

    def test_provided_logger_level_is_unchanged(self) -> None:
        custom = logging.getLogger(_unique("user-app"))
        custom.setLevel(logging.CRITICAL)
        client = Schematic("test-key", config=SchematicConfig(
            offline=True, logger=custom,
        ))
        assert client.logger is custom
        assert client.logger.level == logging.CRITICAL

    def test_log_level_config_ignored_when_logger_provided(self) -> None:
        """If both `logger` and `log_level` are passed, the explicit logger
        wins and its level is untouched."""
        custom = logging.getLogger(_unique("user-app"))
        custom.setLevel(logging.CRITICAL)
        client = Schematic("test-key", config=SchematicConfig(
            offline=True, logger=custom, log_level=logging.DEBUG,
        ))
        assert client.logger.level == logging.CRITICAL  # NOT DEBUG

    async def test_async_provided_logger_level_is_unchanged(self) -> None:
        custom = logging.getLogger(_unique("user-app"))
        custom.setLevel(logging.CRITICAL)
        client = AsyncSchematic("test-key", config=AsyncSchematicConfig(
            offline=True, logger=custom,
        ))
        try:
            assert client.logger is custom
            assert client.logger.level == logging.CRITICAL
        finally:
            await client.shutdown()
