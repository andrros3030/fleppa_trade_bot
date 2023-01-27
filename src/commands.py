"""
Это - прокси файл, для хранения существующих команд в боте
"""
from src.base_modules.routes import DEFAULT_ROUTE, ParsedRoute
from src.base_modules.command import Command
from src.features.feedback_func import feedback_start, feedback_finish
from src.features.reply_function import reply_start, reply_finish
from src.features.public_func import say_wellcome, currency, currency_graph, get_diploma, get_totem
from src.features.support_funcs import set_admin, exec_sql, get_environment, make_link, simulate_crash, make_request
from src.features.basic_func import generate_help, help_with_unmatched, go_back
from src.context import CallContext


class RoutedCommand(Command):
    """
    Расширение команды - команда с путём.
    Если команда не выполняется в одно действие - она должна быть реализована через этот класс
    """

    def __init__(self, alias: list, desc: str, inner_commands=None, admin_only=False, function=None,
                 inner_fields: dict or None = None, # для super
                 route=DEFAULT_ROUTE):
        # TODO: deprecate init function
        super().__init__(alias=alias, desc=desc,
                         inner_commands=inner_commands, admin_only=admin_only,
                         function=function, inner_fields=inner_fields)
        self.route = route

    @classmethod
    def from_command(cls, some_command: Command, route=DEFAULT_ROUTE):
        """
        Конструктор класса из обычной команды и пути

        :param some_command: команда

        :param route: путь
        """
        return RoutedCommand(
            alias=some_command.alias,
            desc=some_command.desc,
            inner_commands=some_command.inner_commands,
            admin_only=some_command.admin_only,
            function=some_command.function,
            route=route,
            inner_fields=some_command.inner_fields
        )

    def match(self, user_querry: str) -> Command or None:
        """
        По хорошему - выбирает необходимую команду для запуска изнутри этой команды
        Если выбрать не удалось - запускает help
        """
        to_grab_all = None
        user_querry = user_querry.split()[0]
        if user_querry[0] == '/' and len(user_querry) > 1:
            user_querry = user_querry[1:]
        for el in self.inner_commands:
            if el.grab_all:
                to_grab_all = el
            elif el.is_callable and user_querry in el.alias:
                return el
        return to_grab_all

    def run(self, message, bot, database, current_route: ParsedRoute, is_admin, logger):
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
        base_route = self.route
        if current_route.route != self.route and self.is_callable:
            executable_command = self
        else:
            executable_command = self.match(message.text)
        if executable_command is None:
            raise Exception(f"Couldn't match function for route: {current_route.route}; and text: {message.text}")
        if type(executable_command) is RoutedCommand:
            base_route = executable_command.route
        return executable_command.function(
            cc=CallContext(
                    message=message,
                    bot=bot,
                    database=database,
                    current_route=current_route,
                    base_route=base_route,  # TODO: кажется можно отказаться в пользу cc.root_command?
                    is_admin=is_admin,
                    logger=logger,
                    root_command=self  # TODO: здесь должен быть предок
                ))


#  region COMMANDS
base_back = Command(
    function=go_back,
    alias=['back', 'назад', 'выход'],
    desc='назад ко всем командам'
)
help_command = Command(
    function=generate_help,
    alias=['help', "помощь", "команды", "доступные команды"],
    desc='что умеет этот бот',
)
all_catcher = Command(
    function=help_with_unmatched,
)
start_command = Command(
    function=say_wellcome,
    alias=['start', "начать"],
    desc='вывести приветственное сообщение',
)
currency_command = RoutedCommand(
    function=currency,
    alias=['currency', "курс валюты"],
    desc='вывести курсы валют и динамику их изменения'
)
totem_command = Command(
    function=get_totem,
    alias=['totem', "тотем", "кто я"],
    desc='узнать свой тотем биржи'
)
diploma_command = RoutedCommand(
    function=get_diploma,
    alias=['diploma', "диплом", "хочу диплом"],
    desc='получить диплом хомяка'
)
currency_graph_command = Command(
    function=currency_graph,
    alias=['currency_graph', "график", "график валют"],
    desc='вывести график курсов валют'
)
crash_command = Command(
    function=simulate_crash,
    alias=['crash'],
    desc='крашнуться',
    admin_only=True
)
env_command = Command(
    function=get_environment,
    alias=['env', 'prod', 'environment', 'среда'],
    desc='вывести тип окружения',
    admin_only=True,
)
db_command = Command(
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
request_command = Command(
    function=make_request,
    alias=['request'],
    desc='отправить запрос',
    admin_only=True
)
make_link_command = Command(
    function=make_link,
    alias=['make_link', 'getlink', 'ссылка', 'start_link'],
    desc='создать ссылку на бота',
    admin_only=True
)
# endregion

# TODO: ограничение по chat_types=['private']


feedback_command = Command(
    function=feedback_start,
    alias=['feedback', "отзыв", "фидбэк", "написать отзыв", "админ"],
    desc='оставить отзыв о работе бота или предложить функциональность',
    inner_fields={'go_back_text': 'Хорошо, буду ждать твой фидбэк в следующий раз :)'},
    inner_commands=[
        Command(
            function=feedback_finish,
            desc='отправить сообщение админам'
        ),
        help_command.copy_with(
            alias=help_command.alias
        ),
        base_back.copy_with(
            desc='вернутся ко всем командам',
            alias=base_back.alias
        )
    ]
)
routed_feedback = RoutedCommand.from_command(feedback_command, route='/feedback')

reply_command = Command(
    function=reply_start,
    alias=['reply'],
    desc='ответить на фидбэк',
    admin_only=True,
    inner_fields={'go_back_text': 'Можно отвечать на другое сообщение'},
    inner_commands=[
        Command(
            function=reply_finish,
            desc='отправить сообщение пользователю'
        ),
        help_command.copy_with(
            alias=help_command.alias
        ),
        base_back.copy_with(
            desc='выйти из команды ответа на сообщение',
            alias=base_back.alias
        )
    ]
)
routed_reply = RoutedCommand.from_command(reply_command, route='/reply')

root_command = Command(
    inner_commands=[
        help_command,
        all_catcher,
        currency_command,
        currency_graph_command,
        totem_command,
        diploma_command,
        routed_feedback,
        start_command,
        crash_command,
        routed_reply,
        set_admin_command,
        env_command,
        db_command,
        make_link_command,
        request_command,
    ],
)

routed_root_command = RoutedCommand.from_command(root_command)

commands_hash_map = {
    routed_root_command.route: routed_root_command,
    routed_feedback.route: routed_feedback,
    routed_reply.route: routed_reply
}

# for el in root_command.inner_commands:
#     if type(el) is RoutedCommand:
#         commands_hash_map[el.route] = el
# TODO: вот тут должна быть бесконечная вложенность. Сделаем через while, когда перейдём на серверную архитектуру
# TODO: провести сравнение скорости работы архитектуры на простом списке и с вот такой вложенностью в словаре
