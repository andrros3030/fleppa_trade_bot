"""
Базовая сущность команды
Базовая сущность не хранит в себе навигационной логики, она представляет только хранилище для данных команды:
псевдонимов, описания, права доступа, внутренние функции

NO PROJECT IMPORTS IN THIS FILE
"""


class Command:
    """
    Базовая сущность команды
    """
    # TODO: подробно описать логику is_callable и grab_all

    def __init__(self, desc: str or None = None, function=None, alias: list or None = None,
                 inner_commands: list or None = None, admin_only=False, inner_fields: dict = None):
        """
        :param alias: набор слов, каждое из которых находясь на первом месте вызовет функцию

        :param desc: описание функции, которое используется при формировании help

        :param function: функция, вызываемая по alias команде (с помощью alias или если grab_all=True)

        :param inner_commands: подкоманды данной команды (дочерние команды)

        :param admin_only: ограничение доступа админам
        """
        self.alias = alias
        self.desc = desc
        self.admin_only = admin_only
        self.inner_commands = inner_commands
        self.function = function
        self.inner_fields = inner_fields

    @property
    def public(self) -> bool:
        """
        :return: доступна ли не админам
        """
        return not self.admin_only

    @property
    def description(self) -> str:
        """
        :return: описание для /help
        """
        if self.public:
            return self.desc
        return f'[ADMIN] {self.desc}'

    @property
    def grab_all(self):
        """
        хочет ли функция работать с любыми сообщениями (если у функции нет псевдонимов)
        """
        return self.alias is None or len(self.alias) == 0

    @property
    def is_callable(self) -> bool:
        return self.function is not None

    @property
    def show_in_help(self) -> bool:
        return self.is_callable and self.desc is not None and len(self.desc) != 0

    def __str__(self):
        """
        Текстовое представление команды для формирования помощи
        """
        # TODO: minor | подставлять тип контента, принимаемого функцией
        if self.grab_all:
            return f'ТЕКСТ — {self.description}'
        return f'/{self.alias[0]} — {self.description}'

    def copy_with(self, desc: str or None = None, alias: list or None = None, inner_fields: dict or None = None):
        """
        Копировать команду с заменой основныъ полей

        :param desc: новое описание

        :param alias: новые псевдонимы

        :param inner_fields: новые внутренние поля

        :return: новый экземпляр команды, с той же самой функцией, подкомандами и правами доступа
        """
        # кажется другие параметры при копировани не должны меняться
        # возможно нужно будет использовать .copy() для корректной работы с не примитивами

        return Command(
            desc=desc,
            alias=alias,
            function=self.function,
            inner_commands=self.inner_commands,
            admin_only=self.admin_only,
            inner_fields=inner_fields
        )
