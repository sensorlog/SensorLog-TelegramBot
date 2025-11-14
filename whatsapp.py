"""
SensorLog-TelegramBot

Este script envia os eventos recebidos para o WhatsApp.
"""

import requests
import logging
from telebot import TeleBot, types
from sensorlog import Decode, Events
from datetime import datetime, timedelta
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CALLMEBOT_API_URL = f"https://api.callmebot.com/whatsapp.php"
bot = TeleBot(token=settings.telegram_token)


def send_get_request(url, data):
    """
    Envia uma solicitação GET para a URL especificada com os dados fornecidos.

    Args:
        url (str): A URL para onde a solicitação GET será enviada.
        data (dict): Os dados a serem enviados como parâmetros na solicitação GET.

    Returns:
        None
    """
    logger.info("Iniciando envio de solicitação GET")
    try:
        logger.info(f"Enviando HTTP/GET para {url} com parâmetros {data}")
        response = requests.get(url, params=data, timeout=10)
        logger.info(f"Resposta do servidor: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"Erro ao enviar solicitação GET: {e}")
    finally:
        logger.info("Finalizado envio de solicitação GET")


def process_channel_message_event(event: Events):
    """
    Processa eventos recebidos do canal do Telegram.

    Args:
        event (Events): Objeto que representa um evento de sensor.
    """
    logger.info("Iniciando processamento do evento")
    try:
        logger.info(f"Processando evento")
        url = CALLMEBOT_API_URL
        diff_time = datetime.now() - event.time
        max_delay = timedelta(minutes=5)
        time = event.time.strftime("\n%d/%m/%Y %H:%M:%S") if diff_time > max_delay else ""
        message = f"*{event.channel_name}*\n{event.text}{time}"
        data = {
            "phone": settings.callmebot_phone,
            "apikey": settings.callmebot_api_key,
            "text": message,
        }
        send_get_request(url, data)
    except Exception as e:
        logger.error(f"Erro ao processar evento: {e}")
    finally:
        logger.info("Finalizando processamento do evento")


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
        if isinstance(message.var_data, Events):
            process_channel_message_event(message.var_data)
    except Exception as e:
        logger.error(f"Erro ao manipular mensagem do canal: {e}")
    finally:
        logger.info("Finalizando manipulação da mensagem do canal")


logger.info("Bot iniciado. Aguardando mensagens do canal")
bot.infinity_polling(skip_pending=False)
