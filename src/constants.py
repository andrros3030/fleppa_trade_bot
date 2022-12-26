import os


DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')
SERVICE_STATIC_KEY = os.getenv('SERVICE_STATIC_KEY')
SERVICE_API_KEY = os.getenv('SERVICE_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK = os.getenv('WEBHOOK')
IS_PRODUCTION = True
SUDO_USERS = [
    439133935,  # Андрей
]


def set_testing_mode():
    # TODO: replace environment variables values here
    global IS_PRODUCTION
    IS_PRODUCTION = False
