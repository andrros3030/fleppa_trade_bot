class Command:
    _alias: list
    _desc: str
    _admin_only: bool

    def __init__(self, alias: list, desc: str, admin_only=False, ):
        self._alias = alias
        self._desc = desc
        self._admin_only = admin_only

    @property
    def commands(self):
        return self._alias

    @property
    def public(self):
        return not self._admin_only


class Commands:
    environment = Command(
        alias=['env', 'prod', 'environment', 'среда'],
        desc='Вывести тип окружения',
        admin_only=True,
    )

    db = Command(
        alias=['sql', 'db'],
        desc='Взаимодействие с базой данных',
        admin_only=True
    )