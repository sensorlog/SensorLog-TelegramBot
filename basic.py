"""
SensorLog-TelegramBot

Este script processa eventos do Telegram e exibe os dados no console.
"""

import logging
from telebot import TeleBot, types
from sensorlog import Decode, Events, Values, EVENT_LEVEL, EVENT_COMMUNICATION
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = TeleBot(token=settings.telegram_token)


def process_channel_message_event(event: Events):
    """
    Processa eventos recebidos do canal do Telegram.

    Args:
        event (Events): Objeto que representa um evento de sensor.

    Eventos:
        - EVENT_LEVEL: Evento relacionado ao nível de algum parâmetro.
        - EVENT_COMMUNICATION: Evento relacionado à comunicação de algum sensor.

    A função imprime detalhes do evento com base no seu tipo.
    """
    logger.info("Iniciando processamento do evento")
    try:
        if event.type == EVENT_LEVEL:
            print(f"Evento de nível:\n{event}")
        elif event.type == EVENT_COMMUNICATION:
            print(f"Evento de comunicação:\n{event}")
        else:
            print(f"Evento desconhecido:\n{event}")
    except Exception as e:
        logger.error(f"Erro ao processar evento: {e}")
    finally:
        logger.info("Finalizando processamento do evento")


def process_channel_message_values(values: Values):
    """
    Processa valores de sensores recebidos do canal do Telegram.

    Args:
        values (Values): Objeto que representa os valores dos sensores.

    A função imprime os valores dos sensores recebidos.
    """
    logger.info("Iniciando processamento dos valores")
    try:
        print(f"Valores de sensores recebidos:\n{values}")
    except Exception as e:
        logger.error(f"Erro ao processar valores: {e}")
    finally:
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
