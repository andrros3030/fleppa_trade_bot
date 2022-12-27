import os

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK = os.getenv('WEBHOOK')
IS_PRODUCTION = True
SUDO_USERS = [
    439133935,  # Андрей
]
context = 'initial context, like NONE'


def set_testing_mode():
    # TODO: replace environment variables values here
    global IS_PRODUCTION
    IS_PRODUCTION = False


def set_context(new_context):
    global context
    context = new_context


def update_db_user_password(new_token):
    global DB_USER_PASSWORD
    DB_USER_PASSWORD = new_token
