import logging
from typing import Union

LogLevel = Union[int, str]
DEFAULT_LOG_LEVEL: int = logging.WARNING

# Name tag for the StreamHandler we attach to the default logger. Lets us
# find and update *our* handler without touching any other handlers a
# consumer may have attached to a same-named logger out-of-band.
_SDK_HANDLER_NAME = "schematichq-default"


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

    sdk_handler = next(
        (h for h in logger.handlers if getattr(h, "name", None) == _SDK_HANDLER_NAME),
        None,
    )
    if sdk_handler is None:
        sdk_handler = logging.StreamHandler()
        sdk_handler.name = _SDK_HANDLER_NAME
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        sdk_handler.setFormatter(formatter)
        logger.addHandler(sdk_handler)
    sdk_handler.setLevel(level)

    return logger
