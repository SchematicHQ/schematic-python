import logging
from typing import Union


LogLevel = Union[int, str]
DEFAULT_LOG_LEVEL: int = logging.WARNING


def get_default_logger(name: str = "schematic", level: LogLevel = DEFAULT_LOG_LEVEL) -> logging.Logger:
    """Build the SDK's default console logger.

    The level defaults to WARNING so production consumers don't get flooded
    with diagnostics they didn't ask for. Pass an explicit level (e.g.
    ``logging.DEBUG`` or ``"DEBUG"``) to enable verbose output. Consumers
    who want full control should pass their own ``logging.Logger`` to the
    Schematic client instead — the SDK leaves that logger's level alone.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    else:
        # Logger already exists (cached by name) — keep the handler in sync
        # with the requested level so a later call with a different level
        # actually takes effect.
        for handler in logger.handlers:
            handler.setLevel(level)

    return logger
