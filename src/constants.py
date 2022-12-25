import os


YDB_ENDPOINT = os.getenv('YDB_ENDPOINT')
YDB_DATABASE = os.getenv('YDB_DATABASE')
SERVICE_STATIC_KEY = os.getenv('SERVICE_STATIC_KEY')
SERVICE_API_KEY = os.getenv('SERVICE_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK = os.getenv('WEBHOOK')
IS_PRODUCTION = True
SUDO_USERS = [
    439133935,  # Андрей
]


def set_testing_mode():
    global IS_PRODUCTION
    IS_PRODUCTION = False
