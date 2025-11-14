"""
SensorLog-TelegramBot
"""

from __future__ import annotations

import sys
from types import ModuleType

from .core import (
    Decode,
    Events,
    Values,
    SetValues,
    Id,
    EVENT_LEVEL,
    EVENT_COMMUNICATION,
    EVENT_UNKNOWN,
    SYMBOL_CHECK,
    SYMBOL_WARNING,
    SYMBOL_DOWN_ARROW,
    SYMBOL_UP_ARROW,
)

__all__ = [
    "Decode",
    "Events",
    "Values",
    "SetValues",
    "Id",
    "EVENT_LEVEL",
    "EVENT_COMMUNICATION",
    "EVENT_UNKNOWN",
]


def _register_compat_module(name: str, attrs: dict):
    full_name = f"{__name__}.{name}"
    module = ModuleType(full_name)
    module.__dict__.update(attrs)
    sys.modules[full_name] = module


_register_compat_module("Values", {"Values": Values})
_register_compat_module("Events", {"Events": Events})
_register_compat_module("Id", {"Id": Id})
_register_compat_module("SetValues", {"SetValues": SetValues})
_register_compat_module(
    "Post",
    {
        "Decode": Decode,
        "EVENT_LEVEL": EVENT_LEVEL,
        "EVENT_COMMUNICATION": EVENT_COMMUNICATION,
        "EVENT_UNKNOWN": EVENT_UNKNOWN,
        "SYMBOL_CHECK": SYMBOL_CHECK,
        "SYMBOL_WARNING": SYMBOL_WARNING,
        "SYMBOL_DOWN_ARROW": SYMBOL_DOWN_ARROW,
        "SYMBOL_UP_ARROW": SYMBOL_UP_ARROW,
    },
)
