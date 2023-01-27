"""
Контекст для запуска бота и контекст для работы команд бота
В основном контекст - это сокращенный вид доступа к какому-либо параметру или свойству запуска.
ONLY BASE AND COMMON MODULES ALLOWED TO BE IMPORTED
"""
import os
import telebot.types
from src.base_modules.db_auth_context import DBAuthContext
from src.base_modules.routes import ParsedRoute
from src.base_modules.logger import Logger
from src.base_modules.totem import Totem
from src.base_modules.command import Command
from src.common_modules.data_source import DataSource


def _mask_token(token: str):
    """
    Функция для маскировки секретов

    :param token: строка, которую необходимо заблюрить

    :returns: безопасное представление секрета
    """
    return token[0:4] + '*' * (len(token) - 5)


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
    bot: telebot.TeleBot
    __message: telebot.types.Message
    current_route: ParsedRoute
    database: DataSource
    logger: Logger
    root_command: Command

    # TODO: нужно ли прокидывать логер через контекст?
    def __init__(self, bot: telebot.TeleBot, database: DataSource,
                 message: telebot.types.Message, is_admin, current_route: ParsedRoute, base_route, logger: Logger,
                 root_command: Command):
        self.is_admin = is_admin
        self.__message = message
        self.bot = bot
        self.database = database
        self.current_route = current_route
        self.base_route = base_route
        self.splitted_message = list(map(lambda el: str(el).lower(), self.text.split()))
        self.logger = logger
        self.totem = Totem(self.message_author)
        self.root_command = root_command

    @property
    def caption(self) -> str or None:
        return self.__message.caption

    @property
    def photo(self):  # TODO: что за тип данных
        return self.__message.photo

    @property
    def sticker(self) -> telebot.types.Sticker or None:
        return self.__message.sticker

    @property
    def content_type(self) -> str:
        return self.__message.content_type

    @property
    def message_author(self) -> int:
        return self.user_data.id

    @property
    def chat_id(self) -> int:
        return self.__message.chat.id

    @property
    def user_data(self) -> telebot.types.User:
        return self.__message.from_user

    @property
    def message_id(self) -> int:
        return self.__message.message_id

    @property
    def text(self) -> str or None:
        return self.__message.text

    @property
    def reply_data(self) -> telebot.types.Message or None:
        return self.__message.reply_to_message

    def __str__(self):
        return str(self.__dict__)


# TODO: тех долг, откзаться от глобальной переменной в пользу DI
global_context = Context()
