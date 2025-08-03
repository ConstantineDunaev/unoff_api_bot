from dotenv import load_dotenv
from os import getenv


class Config:
    load_dotenv()

    TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
    TELEGRAM_USERS = set(int(chat_id.strip()) for chat_id in getenv('TELEGRAM_USERS').split(','))

    MYSQL_HOST = getenv('MYSQL_HOST')
    MYSQL_USER = getenv('MYSQL_USER')
    MYSQL_PASSWORD = getenv('MYSQL_PASSWORD')
    MYSQL_PORT = int(getenv('MYSQL_PORT'))
    MYSQL_SCHEMA = getenv('MYSQL_SCHEMA')
    MYSQL_DUMP = getenv('MYSQL_DUMP')
