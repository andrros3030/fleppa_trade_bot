"""
Это - прокси файл, для хранения существующих команд в боте
"""
from src.base_modules.routes import *
from src.features.public_func import *
from src.features.support_funcs import *
from src.features.public_relations_func import *
from src.context import CallContext
from telebot.types import InlineKeyboardMarkup
from telebot.util import quick_markup


# TODO: кажется, на примере reply_markup и base_route/route -- есть boiler plate
class Command:
    """
    Структура данных "Команда", которая хранит все сведения о команде:
    её путь (вторая точка тригера, помимо псевдонима), имена для вызова (псевдонимы),
    описание, доступна ли только админам, какой тип контента принимает
    """
    _route: str  # если функция не выполняется за одно сообщение - у нее должен быть путь, иначе она работает в корне
    _alias: list  # набор псевдонимов для вызываемой команды
    _desc: str  # описание команды, которое можно отобразить пользователю
    _admin_only: bool  # доступна ли команда только админам
    _accept_text: bool
    _accept_photo: bool
    _accept_sticker: bool

    def __init__(self, alias: list, desc: str, route=DEFAULT_ROUTE, admin_only=False, function=None,
                 accept_text=True, accept_photo=False, accept_sticker=False):
        """
        :param alias: набор слов, каждое из которых находясь на первом месте вызовет функцию
        :param desc: описание функции, которое используется при формировании help
        :param route: путь к функции, если она не отрабатывает за одно сообщение
        :param admin_only: ограничение доступа админам
        :param function: функция, которая вызывается при вызове команды
        :param accept_text: НЕ ИСПОЛЬЗУЕТСЯ ПОКА ЧТО
        :param accept_photo: НЕ ИСПОЛЬЗУЕТСЯ ПОКА ЧТО
        :param accept_sticker: НЕ ИСПОЛЬЗУЕТСЯ ПОКА ЧТО
        """
        self._function = function
        self._alias = alias
        self._desc = desc
        self._admin_only = admin_only
        self._route = route
        self._accept_text = accept_text
        self._accept_photo = accept_photo
        self._accept_sticker = accept_sticker
        self._reply_markup = None

    def with_reply_markup(self, reply_markup: InlineKeyboardMarkup):
        self._reply_markup = reply_markup
        return self

    @property
    def commands(self):
        """
        :return: все псевдонимы команды
        """
        return self._alias

    @property
    def public(self):
        """
        :return: доступна ли не админам
        """
        return not self._admin_only

    @property
    def route(self):
        """
        :return: путь для команды
        """
        return self._route

    @property
    def content_types(self):
        """
        НЕ ИСПОЛЬЗУЕТСЯ ПОКА ЧТО

        :return: массив принимаемых типов контента
        """
        res = []
        if self._accept_sticker:
            res.append('sticker')
        if self._accept_text:
            res.append('text')
        if self._accept_photo:
            res.append('photo')
        return res

    @property
    def description(self):
        """
        :return: описание для /help
        """
        if self.public:
            return self._desc
        return f'[ADMIN] {self._desc}'

    def run(self, bot, database, current_route, is_admin, logger, message=None, query=None):
        """
        Функция для запуска реальной функции команды (должна иметь cc: CallContext в сигнатуре)

        :param message: тригерное сообщение

        :param query: тригерное событие (не сообщение)

        :param bot: объект бота, в который будут отправляться сообщения

        :param database: объект базы данных, с которой работает функция

        :param current_route: распарсеный путь пользователя

        :param is_admin: является ли пользователь админом
        (нужно только в help, остальные функции должны работать одинаково, как для админа, так и для не админа)

        :param logger: объект логера для записи информационных сообщений
        """
        return self._function(
            cc=CallContext(
                query=query,
                message=message,
                bot=bot,
                database=database,
                current_route=current_route,
                base_route=self._route,
                is_admin=is_admin,
                logger=logger,
                reply_markup=self._reply_markup
            )
        )


def generate_help(cc: CallContext):
    """
    Автоматически генерирует сообщение помощи для отображения всех команд

    :param cc: контекст вызова функции
    """
    all_commands = []
    for cmd in commands:
        if cc.is_admin or cmd.public:
            all_commands.append(f'/{cmd.commands[0]} — {cmd.description}')
    res = '\n'.join(all_commands)
    return cc.bot.send_message(cc.chat_id, res)


# TODO: тех долг, откзаться от глобальной переменной в пользу DI
# TODO: ограничение по chat_types=['private']
# TODO: кажется у пользователя не должно быть возможности запускать корневые функции,
# когда он находится в контексте другой функции [/feedback, /reply и др]
# в таком случае route будет вторым тригером для запуска функции, но не ясно, как показать, какие есть подкоманды
# region public commands
# TODO: enforce route for user commands
help_command = Command(
    function=generate_help,
    alias=['help', "помощь", "команды", "доступные команды"],
    desc='список всех команд',
    route=HELP_ROUTE
)
currency_command = Command(
    function=currency,
    alias=['currency', "курс валюты"],
    desc='вывести курсы валют и динамику их изменения',
    route=CURRENCY_ROUTE
)
totem_command = Command(
    function=get_totem,
    alias=['totem', "тотем", "кто я"],
    desc='узнать свой тотем биржи',
    route=TOTEM_ROUTE
)
diploma_command = Command(
    function=get_diploma,
    alias=['diploma', "диплом", "хочу диплом"],
    desc='получить персональный диплом',
    route=DIPLOMA_ROUTE
)
currency_graph_command = Command(
    function=currency_graph,
    alias=['currency_graph', "график", "график валют"],
    desc='вывести график курсов валют',
    route=CURRENCY_GRAPH_ROUTE
)
feedback_command = Command(
    function=feedback,
    alias=['feedback', "отзыв", "фидбэк", "написать отзыв", "админ"],
    desc='оставить отзыв о работе бота или предложить функциональность',
    route=FEEDBACK_ROUTE
)
welcome_command = Command(
    function=say_welcome,
    alias=['start', "начать"],
    desc='вывести приветственное сообщение',
    route=START_ROUTE
)
menu_command = Command(
    function=menu,
    alias=['menu', 'меню', 'домой', 'назад'],
    desc='меню бота',
    route=MENU_ROUTE
)
# endregion
# region admin commands
crash_command = Command(
    function=simulate_crash,
    alias=['crash'],
    desc='крашнуться',
    admin_only=True
)
reply_command = Command(
    function=reply,
    alias=['reply'],
    desc='ответить на фидбэк',
    admin_only=True,
    route='/reply'
)
env_command = Command(
    function=get_environment,
    alias=['env', 'prod', 'environment', 'среда'],
    desc='вывести тип окружения',
    admin_only=True,
)
sql_command = Command(
    function=exec_sql,
    alias=['sql', 'db'],
    desc='взаимодействие с базой данных',
    admin_only=True,
)
set_admin_command = Command(
    function=set_admin,
    alias=['set_admin', 'make_admin', 'do_admin'],
    desc='сделать пользователя админом',
    admin_only=True,
)
make_link_command = Command(
    function=make_link,
    alias=['make_link', 'getlink', 'ссылка', 'start_link'],
    desc='создать ссылку на бота',
    admin_only=True
)
request_command = Command(
    function=make_request,
    alias=['request'],
    desc='отправить запрос',
    admin_only=True
)
# endregion
commands = [
    # public commands >
    menu_command.with_reply_markup(
        quick_markup({
            'Курсы валют': {'callback_data': CURRENCY_ROUTE},
            'Кто я на бирже': {'callback_data': TOTEM_ROUTE},
            'Оставить отзыв': {'callback_data': FEEDBACK_ROUTE}
        })
    ),
    help_command.with_reply_markup(
        quick_markup({
            'Назад к меню': {'callback_data': MENU_ROUTE}
        })
    ),
    welcome_command.with_reply_markup(
        quick_markup({
            'Меню бота': {'callback_data': MENU_ROUTE},
            'Все команды': {'callback_data': HELP_ROUTE}
        })
    ),
    currency_command.with_reply_markup(
        quick_markup({
            'Назад': {'callback_data': MENU_ROUTE}
        })
    ),
    currency_graph_command.with_reply_markup(
        quick_markup({
            'Назад': {'callback_data': MENU_ROUTE}
        })
    ),
    totem_command.with_reply_markup(
        quick_markup({
            "Получить диплом": {'callback_data': DIPLOMA_ROUTE},
            'Назад': {'callback_data': MENU_ROUTE}
        })
    ),
    diploma_command.with_reply_markup(
        quick_markup({
            'Назад': {'callback_data': MENU_ROUTE}
        })
    ),
    feedback_command.with_reply_markup(
        quick_markup({
            'Назад': {'callback_data': MENU_ROUTE}
        })
    ),
    # admin commands >
    crash_command,
    reply_command,
    env_command,
    sql_command,
    set_admin_command,
    make_link_command,
    request_command
]
