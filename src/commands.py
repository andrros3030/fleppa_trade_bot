class Command:
    _route: str
    _alias: list
    _desc: str
    _admin_only: bool

    def __init__(self, alias: list, desc: str, route='/', admin_only=False):
        self._alias = alias
        self._desc = desc
        self._admin_only = admin_only
        self._route = route

    @property
    def commands(self):
        return self._alias

    @property
    def public(self):
        return not self._admin_only

    @property
    def route(self):
        return self._route


class Commands:
    feedback = Command(
        alias=['/feedback'],
        desc='Оставить отзыв о работе бота или предложить функциональность',
        admin_only=False,
        route='/feedback'
    )

    environment = Command(
        alias=['env', 'prod', 'environment', 'среда'],
        desc='Вывести тип окружения',
        admin_only=True,
    )

    db = Command(
        alias=['sql', 'db'],
        desc='Взаимодействие с базой данных',
        admin_only=True,
    )

    set_admin = Command(
        alias=['set_admin', 'make_admin', 'do_admin'],
        desc='Сделать пользователя админом',
        admin_only=True,
    )

    generate_link = Command(
        alias=['make_link', 'getlink', 'ссылка', 'start_link'],
        desc='Создать ссылку на бота',
        admin_only=True
    )
