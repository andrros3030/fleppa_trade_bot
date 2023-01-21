"""
Возможные виды контекста для использования в других модулях
В основном контекст - это сокращенный вид доступа к какому-либо параметру или свойству запуска
NO PROJECT IMPORTS IN THIS FILE
"""
import os


def _mask_token(token: str):
    """
    Функция для маскировки секретов

    :param token: строка, которую необходимо заблюрить

    :returns: безопасное представление секрета
    """
    return token[0:4] + '*' * (len(token) - 5)


class DBAuthContext:
    """
    Контекст для авторизации в базе данных
    """
    def __init__(self, user: str, password: str, host: str, port: str, is_prod: bool, dbname: str = None):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.is_prod = is_prod
        # TODO: посмотреть на логику, кажется она избыточна
        if is_prod:
            self.database = host.split('.')[0]
        else:
            self.dbname = dbname

    @property
    def get_config(self):
        if self.is_prod:
            return f"""
            dbname={self.database}
            host={self.host}
            port={self.port}
            user={self.user}
            password={self.password}
            sslmode=require
            """
        else:
            return f"""
                host={self.host}
                port={self.port}
                dbname={self.dbname}
                user={self.user}
                password={self.password}
                target_session_attrs=read-write
            """


class Context:
    """
    Контекст вызова функции веб-хука или локального запуска бота
    """
    def __init__(self):
        """
        Получение из переменных среды необходимых секретов для подключения ко всем службам
        """
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
        """
        Установка тестового окружения. Если эта функция не была вызвана
        после инициализации контекста - окружение является продовым
        """
        # TODO: replace environment variables values here
        self.IS_PRODUCTION = False

    def set_context(self, new_context):
        """
        Установка контекста запуска функции, работает только в продакшен окружении

        :param new_context: контекст запуска Yandex Cloud Functions
        """
        self.context = new_context

    @property
    def auth_context(self) -> DBAuthContext:
        """
        Сформированные данные для авторизации в yc mdb pg
        Это свойство может быть запрошено до смены контекста на ненулевое значение, keep in mind

        :return: контекст для авторизации в DataSource
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
        """
        Текстовое представление основных параметров контекста запуска

        :return: строка, разделенная \n
        """
        # TODO: сделать для self.context подробный вывод
        token = self.context.token["access_token"] if self.IS_PRODUCTION else self.DB_USER_PASSWORD
        return f"PROD: {self.IS_PRODUCTION}\n" \
               f"CNXT: {self.context}\n" \
               f"DB_TOKEN: {_mask_token(token)}"


class CallContext:
    """
    Контекст вызова одной из команд бота.
    Содержит сокращения для основных атрибутов сообщения.
    Для предотвращения беспорядочного доступа к экземпляру сообщения оно является приватным.
    Хранит экземпляр бота и базы данных, а так же данные о вызове:
    является ли автор сообщения админом, его распарсеный путь, а так же базовый путь команды
    """
    # TODO: нужно ли прокидывать логер через контекст?
    def __init__(self, bot, database, message, is_admin, current_route, base_route):
        self.is_admin = is_admin
        self.__message = message
        self.bot = bot
        self.database = database
        self.current_route = current_route
        self.base_route = base_route
        self.splitted_message = list(map(lambda el: str(el).lower(), self.text.split()))

    @property
    def caption(self):
        return self.__message.caption

    @property
    def photo(self):
        return self.__message.photo

    @property
    def sticker(self):
        return self.__message.sticker

    @property
    def content_type(self):
        return self.__message.content_type

    @property
    def message_author(self):
        return self.user_data.id

    @property
    def chat_id(self):
        return self.__message.chat.id

    @property
    def user_data(self):
        return self.__message.from_user

    @property
    def message_id(self):
        return self.__message.message_id

    @property
    def text(self):
        return self.__message.text

    @property
    def reply_data(self):
        return self.__message.reply_to_message

    def __str__(self):
        return str(self.__dict__)


global_context = Context()
