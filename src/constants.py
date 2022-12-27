import os


class Context:
    def __init__(self):
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_PORT = os.getenv('DB_PORT')
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')
        self.BOT_TOKEN = os.getenv('BOT_TOKEN')
        self.WEBHOOK = os.getenv('WEBHOOK')
        self.IS_PRODUCTION = True
        self.SUDO_USERS = [
            439133935,  # Андрей
        ]
        self.context = 'initial context, like NONE'

    def set_testing_mode(self):
        # TODO: replace environment variables values here
        self.IS_PRODUCTION = False

    def set_context(self, new_context):
        self.context = new_context

    def update_db_user_password(self, new_token):
        self.DB_USER_PASSWORD = new_token


global_context = Context()
