"""
SensorLog-TelegramBot

Este script cria o banco de dados e as tabelas necessárias.
"""

import sqlite3
from config import settings

conn = sqlite3.connect(settings.db_name)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time DATETIME,
    timezone_offset INTEGER,
    channel_id INTEGER,
    channel_name TEXT,
    bot_name TEXT,
    device_name TEXT,
    type INTEGER,
    flag TEXT,
    text TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time DATETIME,
    timezone_offset INTEGER,
    channel_id INTEGER,
    channel_name TEXT,
    bot_name TEXT,
    device_name TEXT,
    level FLOAT,
    raw_level FLOAT,
    distance FLOAT,
    t0 FLOAT,
    t1 FLOAT,
    v0 FLOAT,
    v1 FLOAT,
    snr INTEGER,
    rssi INTEGER,
    snr_gw INTEGER,
    rssi_gw INTEGER,
    counter INTEGER,
    digital_input INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print(f"Banco de dados '{settings.db_name}' e tabelas criadas com sucesso.")
