"""
Базовая сущность команды
Базовая сущность не хранит в себе навигационной логики, она представляет только хранилище для данных команды:
псевдонимов, описания, права доступа, внутренние функции

NO PROJECT IMPORTS IN THIS FILE
"""

# TODO: architecture | grab_all описать логику работы или убрать?

class Command:
    """
    Базовая сущность команды
    """
    _alias: list  # набор псевдонимов для вызываемой команды
    _desc: str  # описание команды, которое можно отобразить пользователю
    _admin_only: bool  # доступна ли команда только админам

    def __init__(self, alias: list, desc: str, function,
                 inner_commands: list or None = None, admin_only=False, grab_all=False):
        """
        :param alias: набор слов, каждое из которых находясь на первом месте вызовет функцию

        :param desc: описание функции, которое используется при формировании help

        :param admin_only: ограничение доступа админам
        """
        self._alias = alias
        self._desc = desc
        self._admin_only = admin_only
        self._inner_commands = inner_commands
        self._grab_all = grab_all
        self.function = function

    @property
    def commands(self) -> list:
        """
        :return: все псевдонимы команды
        """
        return self._alias

    @property
    def public(self) -> bool:
        """
        :return: доступна ли не админам
        """
        return not self._admin_only

    @property
    def description(self) -> str:
        """
        :return: описание для /help
        """
        if self.public:
            return self._desc
        return f'[ADMIN] {self._desc}'

    @property
    def inner_commands(self) -> list or None:
        """
        :return: подкоманды заданной команды
        """
        return self.inner_commands

    def __str__(self):
        """
        Текстовое представление команды для формирования помощи
        """
        return f'/{self.commands[0]} — {self.description}'
