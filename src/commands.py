"""
Это - прокси файл, для хранения существующих команд в боте
"""
import src.base_modules.routes as routing
from src.common_modules.markups import markup_transitions, back_transition, MarkupRoute
import src.features.currency_func as tickers
import src.features.personal_func as personal
import src.features.support_funcs as support
import src.features.communications_func as pr
import src.features.common_func as common
from src.context import CallContext


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

    def __init__(self, alias: list, desc: str, route=routing.DEFAULT_ROUTE, admin_only=False, function=None,
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


def show_preview(cc: CallContext):
    if cc.base_route == '/schedule':
        text = 'Мы работаем над тем, чтобы бот мог уведомить тебя об изменении твоей любимой котировки. ' \
               'Планируем два способа — ежедневное или еженедельное уведомление по твоему расписанию или ' \
               'уведомление об изменении цены. Кажется это полезный функционал, как считаешь?'
    elif cc.base_route == '/stocks':
        text = 'Валюта это самый простой способ вкатиться в мир инвестиций.\n' \
               'Но я ведь не начинающий инвестор! Шлёппа уже большой и скоро будет рассказывать ' \
               'не только про валюту, но и про все остальные котировки на МосБирже. Сейчас разработчики ' \
               'как раз ищут способ, как лучше всего обработать эти данные'
    elif cc.base_route == '/pulse':
        text = 'У желтенького банка кажется тоже есть открытое API. ' \
               'Было бы здорово получить диплом за свои заслуги на бирже или ' \
               'подписаться на изменения акциий из своего портфеля, не правда ли?)\n' \
               'Расскажи, какой другой функционал ты бы хотел видеть в боте'
    else:
        text = 'У нас есть достаточно много идей о графиках. ' \
               'Среди них — свечные графики, различные временные фреймы, ' \
               'линии трендов и лого тикеров.\n' \
               'А ещё, только это секрет, мы готовы презентовать тёмную тему для графиков!)'
    cc.bot.send_message(cc.chat_id, text=text, reply_markup=markup_transitions([
        back_transition,
        MarkupRoute(routing.ParsedRoute(routing.FEEDBACK_ROUTE), text='Предложить свою идею')], drop_this=False))


# TODO: тех долг, откзаться от глобальной переменной в пользу DI
# TODO: ограничение по chat_types=['private']
# region public commands
# TODO: enforce route for user commands || use codgen for this?
help_command = Command(
    function=generate_help,
    alias=['help', "помощь", "команды", "доступные команды"],
    desc='список всех команд',
    route=routing.HELP_ROUTE
)
currency_command = Command(
    function=tickers.currency,
    alias=['currency', "курс", "курсы", "курсы валют", "курс валюты"],
    desc='вывести курсы валют и динамику их изменения',
    route=routing.CURRENCY_ROUTE
)
totem_command = Command(
    function=personal.get_totem,
    alias=['totem', "тотем", "кто я"],
    desc='узнать свой тотем биржи',
    route=routing.TOTEM_ROUTE
)
diploma_command = Command(
    function=personal.get_diploma,
    alias=['diploma', "диплом", "хочу диплом"],
    desc='получить персональный диплом',
    route=routing.DIPLOMA_ROUTE
)
currency_graph_command = Command(
    function=tickers.currency_graph,
    alias=['currency_graph', "график", "график валют"],
    desc='вывести график курсов валют',
    route=routing.CURRENCY_GRAPH_ROUTE
)
feedback_command = Command(
    function=pr.feedback,
    alias=['feedback', "отзыв", "фидбэк", "написать отзыв", "админ"],
    desc='оставить отзыв о работе бота или предложить функциональность',
    route=routing.FEEDBACK_ROUTE
)
welcome_command = Command(
    function=common.say_welcome,
    alias=['start', "начать"],
    desc='вывести приветственное сообщение',
    route=routing.START_ROUTE
)
menu_command = Command(
    function=common.menu,
    alias=['menu', 'меню', 'домой', 'назад'],
    desc='меню бота',
    route=routing.MENU_ROUTE
)
# endregion
# region admin commands
crash_command = Command(
    function=support.simulate_crash,
    alias=['crash'],
    desc='крашнуться',
    admin_only=True
)
reply_command = Command(
    function=pr.reply,
    alias=['reply'],
    desc='ответить на фидбэк',
    admin_only=True,
    route='/reply'
)
env_command = Command(
    function=support.get_environment,
    alias=['env', 'prod', 'environment', 'среда'],
    desc='вывести тип окружения',
    admin_only=True,
)
sql_command = Command(
    function=support.exec_sql,
    alias=['sql', 'db'],
    desc='взаимодействие с базой данных',
    admin_only=True,
    route='/sql'
)
set_admin_command = Command(
    function=support.set_admin,
    alias=['set_admin', 'make_admin', 'do_admin'],
    desc='сделать пользователя админом',
    admin_only=True,
    route='/set_admin'
)
make_link_command = Command(
    function=support.make_link,
    alias=['make_link', 'getlink', 'ссылка', 'start_link'],
    desc='создать ссылку на бота',
    admin_only=True,
    route='/make_link'
)
request_command = Command(
    function=support.make_request,
    alias=['request'],
    desc='отправить запрос',
    admin_only=True,
    route='/request'
)
send_command = Command(
    function=pr.send_to_public,
    alias=['send', 'рассылка'],
    desc='сделать расслыку',
    admin_only=True,
    route=routing.SEND_ROUTE
)
stats_command = Command(
    function=support.stats,
    alias=['stats', 'статистика'],
    desc='статистика по пользователям',
    admin_only=True
)
# endregion
commands = [
    # public commands >
    menu_command,
    help_command,
    welcome_command,
    currency_command,
    currency_graph_command,
    totem_command,
    diploma_command,
    feedback_command,
    # in progress commands>
    Command(
        function=show_preview,
        desc='[В РАЗРАБОТКЕ] подписаться на изменения',
        alias=['schedule'],
        route='/schedule'
    ),
    Command(
        function=show_preview,
        desc='[В РАЗРАБОТКЕ] информация об акциях',
        alias=['stocks'],
        route='/stocks'
    ),
    Command(
        function=show_preview,
        desc='[В РАЗРАБОТКЕ] подключить аккаунт пульса',
        alias=['pulse'],
        route='/pulse'
    ),
    Command(
        function=show_preview,
        desc='[В РАЗРАБОТКЕ] свечные графики торгов',
        alias=['candle'],
        route='/candle'
    ),
    # admin commands >
    crash_command,
    reply_command,
    env_command,
    sql_command,
    set_admin_command,
    make_link_command,
    request_command,
    send_command,
    stats_command
]
