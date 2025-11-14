"""Configurações compartilhadas para os exemplos do SensorLog-TelegramBot.

Os valores podem ser definidos via variáveis de ambiente ou editando este arquivo.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _env(key: str, default: str) -> str:
    return os.getenv(key, default)


@dataclass(frozen=True)
class Settings:
    telegram_token: str = _env("TELEGRAM_TOKEN", "SEU_TOKEN_AQUI")
    event_url: str = _env("EVENT_URL", "http://localhost:9001/events")
    values_url: str = _env("VALUES_URL", "http://localhost:9001/values")
    db_name: str = _env("DB_NAME", "sensordata.db")
    callmebot_api_key: str = _env("CALLMEBOT_API_KEY", "SEU_API_KEY_CALLMEBOT")
    callmebot_phone: str = _env("CALLMEBOT_PHONE", "SEU_NUMERO_TELEFONE")


settings = Settings()
