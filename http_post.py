"""
SensorLog-TelegramBot

Este script envia dados para URLs específicas usando HTTP POST.
"""

import requests
import logging
import json
from telebot import TeleBot, types
from sensorlog import Decode, Events, Values

# Detalhes sobre a API do telegram
# https://core.telegram.org/bots/api

# Detalhes sobre a lib telebot
# https://github.com/eternnoir/pyBotAPI

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Substitua o token pelo seu token criado com o BotFather (https://t.me/BotFather)
TELEGRAM_TOKEN = "SEU_TOKEN_AQUI"
EVENT_URL = "http://localhost:9001/events"  # Substitua pela URL desejada
VALUES_URL = "http://localhost:9001/values"  # Substitua pela URL desejada
# Adicione seu bot num canal de LOG.
# Quando uma publicação de evento for publicada, a função process_channel_message_event
# será chamada com o evento do sensor.
# Quando uma publicação de valores de sensor for publicada, a função process_channel_message_values
# será chamada com os valores dos sensores

bot = TeleBot(token=TELEGRAM_TOKEN)


def send_post_request(url, data):
    """
    Envia uma solicitação POST para a URL especificada com os dados fornecidos.

    Args:
        url (str): A URL para onde a solicitação POST será enviada.
        data (str): Os dados a serem enviados na solicitação POST.

    Returns:
        None
    """
    logger.info("Iniciando envio de solicitação POST")
    try:
        json_data = json.dumps(data)
        logger.info(f"Enviando HTTP/POST para {url} com dados {json_data}")
        response = requests.post(url, json=json_data, timeout=10)
        logger.info(f"Resposta do servidor: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"Erro ao enviar solicitação POST: {e}")
    finally:
        logger.info("Finalizado envio de solicitação POST")


def process_channel_message_event(event: Events):
    """
    Processa eventos recebidos do canal do Telegram.

    Args:
        event (Events): Objeto que representa um evento de sensor.
    """
    logger.info("Iniciando processamento do evento")
    try:
        logger.info(f"Processando evento")
        url = EVENT_URL
        data = {
            "time": event.time.timestamp(),
            "timezone_offset": event.timezone_offset.total_seconds(),
            "channel_id": event.channel_id,
            "channel_name": event.channel_name,
            "bot_name": event.bot_name,
            "device_name": event.device_name,
            "type": event.type,
            "flag": event.flag,
            "text": event.text,
        }
        send_post_request(url, data)
    except Exception as e:
        logger.error(f"Erro ao processar evento: {e}")
    finally:
        logger.info("Finalizando processamento do evento")


def process_channel_message_values(values: Values):
    """
    Processa valores de sensores recebidos do canal do Telegram.

    Args:
        values (Values): Objeto que representa os valores dos sensores.
    """
    logger.info("Iniciando processamento dos valores")
    try:
        logger.info(f"Processando valores")
        url = VALUES_URL
        data = {
            "time": values.time.timestamp(),
            "timezone_offset": values.timezone_offset.total_seconds(),
            "channel_id": values.channel_id,
            "channel_name": values.channel_name,
            "bot_name": values.bot_name,
            "device_name": values.device_name,
            "level": values.level,
            "raw_level": values.raw_level,
            "distance": values.distance,
            "t0": values.t0,
            "t1": values.t1,
            "v0": values.v0,
            "v1": values.v1,
            "snr": values.snr,
            "rssi": values.rssi,
            "snr_gw": values.snr_gw,
            "rssi_gw": values.rssi_gw,
            "counter": values.counter,
            "digital_input": values.digital_input,
        }
        send_post_request(url, data)
    except Exception as e:
        logger.error(f"Erro ao processar valores: {e}")
    logger.info("Finalizando processamento dos valores")


def filter_direct_channel_text_signed(m: types.Message) -> bool:
    """
    Filtra mensagens de texto diretas assinadas em um canal.

    Args:
        m (types.Message): A mensagem recebida do canal do Telegram.

    Returns:
        bool: True se a mensagem atender aos critérios de filtro, False caso contrário.
    """
    return (
        m.reply_to_message is None
        and m.forward_from_chat is None
        and m.author_signature is not None
        and m.content_type == "text"
        and m.chat.type == "channel"
    )


@bot.channel_post_handler(func=filter_direct_channel_text_signed)
def handle_channel_message(m: types.Message):
    """
    Manipula postagens de canal filtradas.

    Args:
        m (types.Message): A mensagem recebida do canal do Telegram.
    """
    logger.info("Iniciando manipulação da mensagem do canal")
    try:
        message = Decode(m)
        if isinstance(message.var_data, Values):
            process_channel_message_values(message.var_data)
        elif isinstance(message.var_data, Events):
            process_channel_message_event(message.var_data)
    except Exception as e:
        logger.error(f"Erro ao manipular mensagem do canal: {e}")
    finally:
        logger.info("Finalizando manipulação da mensagem do canal")


logger.info("Bot iniciado. Aguardando mensagens do canal")
bot.infinity_polling(skip_pending=False)
