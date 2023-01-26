"""
Это - прокси файл, для хранения существующих команд в боте
"""
from src.base_modules.routes import DEFAULT_ROUTE
from src.base_modules.command import Command
from src.features.public_func import feedback, reply, say_wellcome, currency, currency_graph, get_diploma, get_totem
from src.features.support_funcs import set_admin, exec_sql, get_environment, make_link, simulate_crash, make_request
from src.context import CallContext


class RoutedCommand(Command):
    _route: str  # если функция не выполняется за одно сообщение - у нее должен быть путь, иначе она работает в корне

    def __init__(self, alias: list, desc: str, inner_commands=None, admin_only=False, function=None,  # для super
                 route=DEFAULT_ROUTE, block_back=False):
        super().__init__(alias=alias, desc=desc,
                         inner_commands=inner_commands, admin_only=admin_only, function=function)
        self._route = route
        self._block_back = block_back

    @property
    def route(self) -> str:
        """
        :return: путь для команды
        """
        return self._route

    def match(self, inner_command_alias) -> Command or None:
        """
        По хорошему - выбирает необходимую команду для запуска изнутри этой команды
        Если выбрать не удалось - запускает help
        """
        pass

    def run(self, message, bot, database, current_route, is_admin, logger):
        """
        Функция для запуска реальной функции команды (должна иметь cc: CallContext в сигнатуре)

        :param message: тригерное сообщение

        :param bot: объект бота, в который будут отправляться сообщения

        :param database: объект базы данных, с которой работает функция

        :param current_route: распарсеный путь пользователя

        :param is_admin: является ли пользователь админом
        (нужно только в help, остальные функции должны работать одинаково, как для админа, так и для не админа)

        :param logger: объект логера для записи информационных сообщений
        """
        return self.function(
            cc=CallContext(
                message=message,
                bot=bot,
                database=database,
                current_route=current_route,
                base_route=self._route,
                is_admin=is_admin,
                logger=logger
            )
        )


# TODO: architecture | move function somewhere inside?
def generate_help(cc: CallContext):
    """
    Автоматически генерирует сообщение помощи для отображения всех команд

    :param cc: контекст вызова функции
    """
    all_commands = []
    if cc.current_route.route == DEFAULT_ROUTE:
        for cmd in commands:
            if cc.is_admin or cmd.public:
                all_commands.append(str(cmd))
    else:
        # TODO: architecture | iterate over inner commands of command
        pass
    res = '\n'.join(all_commands)
    return cc.bot.send_message(cc.chat_id, res)


# TODO: тех долг, откзаться от глобальной переменной в пользу DI
# TODO: ограничение по chat_types=['private']
commands = [
    RoutedCommand(
        function=generate_help,
        alias=['help', "помощь", "команды", "доступные команды"],
        desc='что умеет этот бот'
    ),
    RoutedCommand(
        function=say_wellcome,
        alias=['start', "начать"],
        desc='вывести приветственное сообщение',
    ),
    RoutedCommand(
        function=currency,
        alias=['currency', "курс валюты"],
        desc='вывести курсы валют и динамику их изменения'
    ),
    RoutedCommand(
        function=get_totem,
        alias=['totem', "тотем", "кто я"],
        desc='узнать свой тотем биржи'
    ),
    RoutedCommand(
        function=get_diploma,
        alias=['diploma', "диплом", "хочу диплом"],
        desc='получить диплом хомяка'
    ),
    RoutedCommand(
        function=currency_graph,
        alias=['currency_graph', "график", "график валют"],
        desc='вывести график курсов валют'
    ),
    RoutedCommand(
        function=feedback,
        alias=['feedback', "отзыв", "фидбэк", "написать отзыв", "админ"],
        desc='оставить отзыв о работе бота или предложить функциональность',
        route='/feedback'
    ),
    RoutedCommand(
        function=simulate_crash,
        alias=['crash'],
        desc='крашнуться',
        admin_only=True
    ),
    RoutedCommand(
        function=reply,
        alias=['reply'],
        desc='ответить на фидбэк',
        admin_only=True,
        route='/reply'
    ),
    RoutedCommand(
        function=get_environment,
        alias=['env', 'prod', 'environment', 'среда'],
        desc='вывести тип окружения',
        admin_only=True,
    ),
    RoutedCommand(
        function=exec_sql,
        alias=['sql', 'db'],
        desc='взаимодействие с базой данных',
        admin_only=True,
    ),
    RoutedCommand(
        function=set_admin,
        alias=['set_admin', 'make_admin', 'do_admin'],
        desc='сделать пользователя админом',
        admin_only=True,
    ),
    RoutedCommand(
        function=make_link,
        alias=['make_link', 'getlink', 'ссылка', 'start_link'],
        desc='создать ссылку на бота',
        admin_only=True
    ),
    RoutedCommand(
        function=make_request,
        alias=['request'],
        desc='отправить запрос',
        admin_only=True
    )
]
