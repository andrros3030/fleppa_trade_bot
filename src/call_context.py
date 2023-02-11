"""
Контекст для работы команд бота.
В основном контекст - это сокращенный вид доступа к какому-либо параметру или свойству вызова.

ONLY BASE AND COMMON MODULES ALLOWED TO BE IMPORTED
"""
import telebot.types
from src.base_modules.routes import ParsedRoute, DATA_ARG
from src.base_modules.logger import Logger
from src.base_modules.totem import Totem
from src.common_modules.data_source import DataSource
from src.common_modules.run_context import Context


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
    __query: telebot.types.CallbackQuery
    current_route: ParsedRoute
    database: DataSource
    logger: Logger

    def __init__(self, bot: telebot.TeleBot, database: DataSource, env_context: Context,
                 is_admin, current_route: ParsedRoute, base_route, logger: Logger,
                 message: telebot.types.Message = None, query: telebot.types.CallbackQuery = None
                 ):
        self.logger = logger
        self.bot = bot
        self.database = database
        self.env_context = env_context
        self.is_admin = is_admin
        self.__message = message
        self.__query = query
        self.current_route = current_route
        self.base_route = base_route
        self.totem = Totem(self.message_author)

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
        if self.__message is None:
            return self.__query.message.chat.id
        return self.__message.chat.id

    @property
    def user_data(self) -> telebot.types.User:
        if self.__message is None:
            return self.__query.from_user
        return self.__message.from_user

    @property
    def message_id(self) -> int:
        return self.__message.message_id

    @property
    def text(self) -> str or None:
        if self.__message is None:
            parsed_data = ParsedRoute(self.__query.data)
            return parsed_data.get_arg(DATA_ARG)
        return self.__message.text

    @property
    def reply_data(self) -> telebot.types.Message or None:
        if type(self.__message) is not telebot.types.Message:
            return None
        return self.__message.reply_to_message

    @property
    def base_trigger(self) -> bool:
        """
        Был ли вызван первый этап команды или уже есть параметры вызова
        Если текст пустой (признак вызова из inline без стандартного текстового параметра)
        или если сообщение не пустое (вызов текстом) и путь пользователя не совпадает с базовым путём команды
        """
        return (self.__message is not None and self.current_route != self.base_route) or self.text is None

    def focus(self, new_route=None):
        """
        Захватить ввод этой командой
        """
        if new_route is None:
            new_route = self.base_route
        return self.database.set_route(user_id=self.message_author, route=str(new_route))

    def unfocus(self):
        """
        Отпустить захват ввода с команды
        """
        self.database.set_route(self.message_author)

    def __str__(self):
        return str(self.__dict__)
