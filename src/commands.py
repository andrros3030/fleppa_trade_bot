from src.routes import DEFAULT_ROUTE
from src.public_func import feedback, reply, say_wellcome, currency
from src.support_funcs import set_admin, exec_sql, get_environment, make_link, simulate_crash
from src.constants import CallContext


class Command:
    _route: str  # если функция не выполняется за одно сообщение - у нее должен быть путь, иначе она работает в корне
    _alias: list  # набор псевдонимов для вызываемой команды
    _desc: str  # описание команды, которое можно отобразить пользователю
    _admin_only: bool  # доступна ли команда только админам
    _accept_text: bool
    _accept_photo: bool
    _accept_sticker: bool

    def __init__(self, alias: list, desc: str, route=DEFAULT_ROUTE, admin_only=False, function=None,
                 accept_text=True, accept_photo=False, accept_sticker=False):
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
        return self._alias

    @property
    def public(self):
        return not self._admin_only

    @property
    def route(self):
        return self._route

    @property
    def content_types(self):
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
        if self.public:
            return self._desc
        return f'[ADMIN] {self._desc}'

    def run(self, message, bot, database, current_route, is_admin):
        return self._function(
            cc=CallContext(
                chat_id=message.chat.id,
                message_author=message.from_user.id,
                bot=bot,
                database=database,
                message_id=message.message_id,
                text=message.text,
                reply_data=message.reply_to_message,
                content_type=message.content_type,
                current_route=current_route,
                sticker=message.sticker,
                photo=message.photo,
                caption=message.caption,
                base_route=self._route,
                is_admin=is_admin
            )
        )


def generate_help(cc: CallContext):
    all_commands = []
    for key, value in commands.items():
        if cc.is_admin or value.public:
            all_commands.append(f'/{value.commands[0]} — {value.description}')
    res = '\n'.join(all_commands)
    return cc.bot.send_message(cc.chat_id, res)


# TODO: ограничение по chat_types=['private']
commands = {
    'help': Command(
        function=generate_help,
        alias=['help'],
        desc='Что умеет этот бот'
    ),
    'start': Command(
        function=say_wellcome,
        alias=['start'],
        desc='вывести приветственное сообщение',
    ),
    'currency': Command(
        function=currency,
        alias=['currency'],
        desc='вывести курсы валют и динамику их изменения'
    ),
    'crash': Command(
        function=simulate_crash,
        alias=['crash'],
        desc='крашнуться',
        admin_only=True
    ),
    'reply': Command(
        function=reply,
        alias=['reply'],
        desc='ответить на фидбэк',
        admin_only=True,
        route='reply'
    ),
    'feedback': Command(
        function=feedback,
        alias=['feedback'],
        desc='оставить отзыв о работе бота или предложить функциональность',
        route='/feedback'
    ),
    'environment': Command(
        function=get_environment,
        alias=['env', 'prod', 'environment', 'среда'],
        desc='вывести тип окружения',
        admin_only=True,
    ),
    'db': Command(
        function=exec_sql,
        alias=['sql', 'db'],
        desc='взаимодействие с базой данных',
        admin_only=True,
    ),
    'set_admin': Command(
        function=set_admin,
        alias=['set_admin', 'make_admin', 'do_admin'],
        desc='сделать пользователя админом',
        admin_only=True,
    ),
    'generate_link': Command(
        function=make_link,
        alias=['make_link', 'getlink', 'ссылка', 'start_link'],
        desc='создать ссылку на бота',
        admin_only=True
    )
}
