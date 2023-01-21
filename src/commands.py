"""
Это - прокси файл, для хранения существующих команд в боте
"""
from src.base_modules.routes import DEFAULT_ROUTE
from src.public_func import feedback, reply, say_wellcome, currency, currency_graph, get_diploma
from src.support_funcs import set_admin, exec_sql, get_environment, make_link, simulate_crash, make_request
from src.base_modules.context import CallContext


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

    def run(self, message, bot, database, current_route, is_admin):
        """
        Функция для запуска реальной функции команды (должна иметь cc: CallContext в сигнатуре)

        :param message: тригерное сообщение
        :param bot: объект бота, в который будут отправляться сообщения
        :param database: объект базы данных, с которой работает функция
        :param current_route: распарсеный путь пользователя
        :param is_admin: является ли пользователь админом
        (нужно только в help, остальные функции должны работать одинаково, как для админа, так и для не админа)
        """
        return self._function(
            cc=CallContext(
                message=message,
                bot=bot,
                database=database,
                current_route=current_route,
                base_route=self._route,
                is_admin=is_admin
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


# TODO: ограничение по chat_types=['private']
# TODO: кажется у пользователя не должно быть возможности запускать корневые функции,
# когда он находится в контексте другой функции [/feedback, /reply и др]
# в таком случае route будет вторым тригером для запуска функции, но не ясно, как показать, какие есть подкоманды
commands = [
    Command(
        function=generate_help,
        alias=['help'],
        desc='что умеет этот бот'
    ),
    Command(
        function=say_wellcome,
        alias=['start'],
        desc='вывести приветственное сообщение',
    ),
    Command(
        function=currency,
        alias=['currency'],
        desc='вывести курсы валют и динамику их изменения'
    ),
    Command(
        function=get_diploma,
        alias=['diploma'],
        desc='получить диплом хомяка'
    ),
    Command(
        function=currency_graph,
        alias=['currency_graph'],
        desc='вывести график курсов валют'
    ),
    Command(
        function=feedback,
        alias=['feedback'],
        desc='оставить отзыв о работе бота или предложить функциональность',
        route='/feedback'
    ),
    Command(
        function=simulate_crash,
        alias=['crash'],
        desc='крашнуться',
        admin_only=True
    ),
    Command(
        function=reply,
        alias=['reply'],
        desc='ответить на фидбэк',
        admin_only=True,
        route='/reply'
    ),
    Command(
        function=get_environment,
        alias=['env', 'prod', 'environment', 'среда'],
        desc='вывести тип окружения',
        admin_only=True,
    ),
    Command(
        function=exec_sql,
        alias=['sql', 'db'],
        desc='взаимодействие с базой данных',
        admin_only=True,
    ),
    Command(
        function=set_admin,
        alias=['set_admin', 'make_admin', 'do_admin'],
        desc='сделать пользователя админом',
        admin_only=True,
    ),
    Command(
        function=make_link,
        alias=['make_link', 'getlink', 'ссылка', 'start_link'],
        desc='создать ссылку на бота',
        admin_only=True
    ),
    Command(
        function=make_request,
        alias=['request'],
        desc='отправить запрос',
        admin_only=True
    )
]
