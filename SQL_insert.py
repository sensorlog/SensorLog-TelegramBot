import sqlite3
import logging
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
DB_NAME = "sensordata.db"

# Adicione seu bot num canal de LOG.
# Quando um sensor fizer alguma Evento o método process_post_event será chamado
# com o evento de notificação do sensor.
# Quando uma publicação de valores de sensor for publicada,
# o método process_post_values será chamado com os valores dos sensores

bot = TeleBot(token=TELEGRAM_TOKEN)


def insert_into_db(table, data):
    """
    Insere dados em uma tabela do banco de dados SQLite.

    Args:
        table (str): O nome da tabela onde os dados serão inseridos.
        data (dict): Os dados a serem inseridos na tabela.

    Returns:
        None
    """
    logger.info("Iniciando inserção no banco de dados")
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor.execute(sql, tuple(data.values()))
        conn.commit()
        conn.close()
        logger.info(f"Dados inseridos na tabela {table}: {data}")
    except Exception as e:
        logger.error(f"Erro ao inserir dados no banco de dados: {e}")
    logger.info("Finalizando inserção no banco de dados")


def process_post_event(event: Events):
    """
    Processa eventos recebidos do canal do Telegram.

    Args:
        event (Events): Objeto que representa um evento de sensor.

    A função insere os dados do evento na tabela 'events' do banco de dados.
    """
    logger.info("Iniciando processamento do evento")
    try:
        logger.info(f"Processando evento")
        data = {
            "time": event.time,
            "timezone_offset": event.timezone_offset.total_seconds(),
            "channel_id": event.channel_id,
            "channel_name": event.channel_name,
            "bot_name": event.bot_name,
            "device_name": event.device_name,
            "type": event.type,
            "flag": event.flag,
            "text": event.text,
        }
        insert_into_db("events", data)
    except Exception as e:
        logger.error(f"Erro ao processar evento: {e}")
    logger.info("Finalizando processamento do evento")


def process_post_values(values: Values):
    """
    Processa valores de sensores recebidos do canal do Telegram.

    Args:
        values (Values): Objeto que representa os valores dos sensores.

    A função insere os valores dos sensores na tabela 'sensor_values' do banco de dados.
    """
    logger.info("Iniciando processamento dos valores")
    try:
        logger.info(f"Processando valores")
        data = {
            "time": values.time,
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
        }
        insert_into_db("sensor_values", data)
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
def handle_channel_post(m: types.Message):
    """
    Manipula postagens de canal filtradas.

    Args:
        m (types.Message): A mensagem recebida do canal do Telegram.

    A função decodifica a mensagem e processa os dados de eventos ou valores dos sensores.
    """
    logger.info("Iniciando manipulação da mensagem do canal")
    try:
        message = Decode(m)
        if isinstance(message.var_data, Values):
            process_post_values(message.var_data)
        elif isinstance(message.var_data, Events):
            process_post_event(message.var_data)
    except Exception as e:
        logger.error(f"Erro ao manipular mensagem do canal: {e}")
    logger.info("Finalizando manipulação da mensagem do canal")


logger.info("Bot iniciado. Aguardando mensagens do canal")
bot.infinity_polling(skip_pending=False)
