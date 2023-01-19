import os
from src.data_source import DBAuthContext


def mask_token(token: str):
    return token[0:4] + '*' * (len(token) - 5)


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
        self.FEEDBACK_CHAT_ID = [
            -898292404,  # Фидбэчница
        ]
        self.context = None

    def set_testing_mode(self):
        # TODO: replace environment variables values here
        self.IS_PRODUCTION = False

    def set_context(self, new_context):
        self.context = new_context

    def update_db_user_password(self, new_token):
        self.DB_USER_PASSWORD = new_token

    @property
    def auth_context(self) -> DBAuthContext:
        """
        Сформированные данные для авторизации в yc mdb pg
        Это свойство может быть запрошено до смены контекста на ненулевое значение, keep in mind
        :return:
        контекст для авторизации в DataSource
        """
        return DBAuthContext(
            user=self.DB_USER,
            password=self.context.token["access_token"] if self.IS_PRODUCTION else self.DB_USER_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            is_prod=self.IS_PRODUCTION,
            dbname=self.DB_NAME,
        )

    def __str__(self):
        token = self.context.token["access_token"] if self.IS_PRODUCTION else self.DB_USER_PASSWORD
        return f"PROD: {self.IS_PRODUCTION}\n" \
               f"CNXT: {self.context}\n" \
               f"DB_TOKEN: {mask_token(token)}"


class CallContext:
    def __init__(self, chat_id, message_author, bot, database, message_id, text, is_admin,
                 reply_data, content_type, current_route, sticker, photo, caption, base_route):
        self.chat_id = chat_id
        self.message_author = message_author
        self.bot = bot
        self.database = database
        self.message_id = message_id
        self.text = text
        self.reply_data = reply_data
        self.content_type = content_type
        self.current_route = current_route
        self.sticker = sticker
        self.photo = photo
        self.caption = caption
        self.base_route = base_route
        self.splitted_message = list(map(lambda el: str(el).lower(), text.split())),
        self.is_admin = is_admin

    def __str__(self):
        return str(self.__dict__)


global_context = Context()
