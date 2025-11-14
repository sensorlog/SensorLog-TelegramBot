"""
Núcleo compacto da biblioteca sensorlog.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Callable, Optional

from telebot import types

SYMBOL_CHECK = "\u2705"
SYMBOL_WARNING = "\u26A0"
SYMBOL_DOWN_ARROW = "\u2B07"
SYMBOL_UP_ARROW = "\u2B06"
EVENT_SYMBOLS = (SYMBOL_CHECK, SYMBOL_WARNING, SYMBOL_DOWN_ARROW, SYMBOL_UP_ARROW)

EVENT_UNKNOWN = 0
EVENT_LEVEL = 1
EVENT_COMMUNICATION = 2

VALUE_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")

_IDENTIFICATION_FIELDS = (
    "time",
    "timezone_offset",
    "channel_id",
    "channel_name",
    "message_id",
    "bot_id",
    "bot_name",
    "device_id",
    "device_name",
)
_VALUE_FIELDS = (
    "level",
    "raw_level",
    "distance",
    "t0",
    "t1",
    "v0",
    "v1",
    "snr",
    "rssi",
    "snr_gw",
    "rssi_gw",
    "speed1",
    "speed2",
    "counter",
    "digital_input",
)


def _coerce_time(value: datetime | int | None) -> datetime:
    if value is None:
        return datetime.now()
    if isinstance(value, datetime):
        return value
    if isinstance(value, int):
        return datetime.fromtimestamp(value)
    raise ValueError("Invalid type for 'time'. Expected datetime or int.")


def _coerce_tz(value: timedelta | int | None) -> timedelta:
    if value is None:
        return timedelta()
    if isinstance(value, timedelta):
        return value
    if isinstance(value, int):
        return timedelta(seconds=value)
    raise ValueError("Invalid type for 'timezone_offset'. Expected timedelta or int.")


class Id:
    """Metadados comuns a valores e eventos."""

    __slots__ = (
        "__time",
        "__timezone_offset",
        "channel_id",
        "channel_name",
        "message_id",
        "bot_id",
        "bot_name",
        "device_id",
        "device_name",
    )

    def __init__(
        self,
        time: Optional[datetime | int] = None,
        timezone_offset: Optional[timedelta | int] = timedelta(),
        channel_id: Optional[int] = None,
        channel_name: Optional[str] = None,
        message_id: Optional[int] = None,
        bot_id: Optional[int] = None,
        bot_name: Optional[str] = None,
        device_id: Optional[int] = None,
        device_name: Optional[str] = None,
    ):
        self.time = time
        self.timezone_offset = timezone_offset
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.message_id = message_id
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.device_id = device_id
        self.device_name = device_name

    @property
    def time(self) -> datetime:
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = _coerce_time(value)

    @property
    def timezone_offset(self) -> timedelta:
        return self.__timezone_offset

    @timezone_offset.setter
    def timezone_offset(self, value):
        self.__timezone_offset = _coerce_tz(value)

    def __str__(self):
        return "".join(f"  {field}: {getattr(self, field)}\n" for field in _IDENTIFICATION_FIELDS)


class Events(Id):
    """Representa alertas ou notificações dos sensores."""

    __slots__ = ("type", "flag", "text")

    def __init__(self, event_type: int, event_text: str, event_flag: str = "", **kwargs):
        super().__init__(**kwargs)
        self.type = event_type
        self.flag = event_flag
        self.text = event_text

    def __str__(self):
        return (
            f"{super().__str__()}"
            f"  type: {self.type}\n"
            f"  flag: {self.flag}\n"
            f"  text: {self.text}"
        )


class Values(Id):
    """Leituras periódicas dos dispositivos."""

    __slots__ = _VALUE_FIELDS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for field in _VALUE_FIELDS:
            setattr(self, field, None)

    def __str__(self):
        id_repr = "".join(f"  {field}: {getattr(self, field)}\n" for field in _IDENTIFICATION_FIELDS)
        value_repr = "".join(f"  {field}: {getattr(self, field)}\n" for field in _VALUE_FIELDS)
        return f"{id_repr}{value_repr.rstrip()}"


def _float(value) -> float:
    return float(value)


def _int(value) -> int:
    return int(float(value))


def _digital(value) -> int:
    normalized = str(value).strip().lower()
    if normalized.startswith("abert"):
        return 1
    if normalized.startswith("fech"):
        return 0
    return _int(normalized)


class SetValues(Values):
    """Traduz pares texto→atributo."""

    __slots__ = ()

    __TRANSLATE: dict[str, tuple[str, Callable]] = {
        "Nível": ("level", _float),
        "Nível*": ("raw_level", _float),
        "Dist₍₀₎": ("distance", _float),
        "T0": ("t0", _float),
        "T1": ("t1", _float),
        "V0": ("v0", _float),
        "V1": ("v1", _float),
        "SNR": ("snr", _int),
        "RSSI": ("rssi", _int),
        "SNR(gw)": ("snr_gw", _int),
        "RSSI(gw)": ("rssi_gw", _int),
        "Δd/Δt₍₋₁₎": ("speed1", _int),
        "Δd/Δt₍₋₂₎": ("speed2", _int),
        "Contador": ("counter", _int),
        "Entrada Digital": ("digital_input", _digital),
    }

    def set_value(self, key: str, value) -> bool:
        entry = self.__TRANSLATE.get(key)
        if not entry:
            return False
        attr, caster = entry
        setattr(self, attr, caster(value))
        return True


class Decode:
    """
    Interpreta mensagens do Telegram e produz Values ou Events.
    """

    __slots__ = ("var_data",)

    def __init__(self, message: types.Message):
        self.var_data: Optional[Values | Events] = None
        self._decode(message)

    def _decode(self, message: types.Message):
        lines = (message.text or "").splitlines()
        if not lines:
            return
        self.var_data = self._parse_values(lines, message) or self._parse_event(lines, message)

    @staticmethod
    def _parse_values(lines: list[str], message: types.Message) -> Optional[Values]:
        match = re.search(r'Nome:\s*"([^"]+)"', lines[0])
        if not match:
            return None

        result = SetValues(
            device_name=match.group(1).strip(),
            time=message.date,
            channel_id=message.chat.id,
            channel_name=message.chat.title,
            message_id=message.message_id,
            bot_name=message.author_signature,
        )

        for line in lines[1:]:
            key_value = line.split(":", 1)
            if len(key_value) != 2:
                continue
            key = key_value[0].strip()
            raw_value = key_value[1].strip()
            parsed_value = Decode._extract_value(raw_value)
            try:
                result.set_value(key, parsed_value)
            except (ValueError, TypeError):
                continue
        return result

    @staticmethod
    def _parse_event(lines: list[str], message: types.Message) -> Optional[Events]:
        if len(lines) < 2:
            return None

        splitted = lines[0].split(":", 1)
        if len(splitted) != 2:
            return None

        device_name, text_of_alert = splitted[0].strip(), splitted[1].strip()
        if not device_name or not text_of_alert:
            return None

        event_flag = "".join(symbol for symbol in text_of_alert if symbol in EVENT_SYMBOLS)
        if not event_flag:
            return None

        event_text = lines[1].strip()
        lowered = event_text.lower()
        if "nível" in lowered:
            event_type = EVENT_LEVEL
        elif "comunicação" in lowered:
            event_type = EVENT_COMMUNICATION
        else:
            return None

        return Events(
            device_name=device_name,
            event_flag=event_flag,
            time=message.date,
            channel_id=message.chat.id,
            channel_name=message.chat.title,
            message_id=message.message_id,
            bot_name=message.author_signature,
            event_type=event_type,
            event_text=f"{lines[0]}\n{lines[1]}",
        )

    @staticmethod
    def _extract_value(raw_value: str):
        match = VALUE_PATTERN.search(raw_value)
        return match.group() if match else raw_value.strip()


__all__ = [
    "Decode",
    "Events",
    "Values",
    "SetValues",
    "Id",
    "EVENT_LEVEL",
    "EVENT_COMMUNICATION",
    "EVENT_UNKNOWN",
    "SYMBOL_CHECK",
    "SYMBOL_WARNING",
    "SYMBOL_DOWN_ARROW",
    "SYMBOL_UP_ARROW",
]
