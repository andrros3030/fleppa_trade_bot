"""
В этом файле описана логика работы с путями, которые мы храним для каждого пользователя
+ константные пути для команд
NO PROJECT IMPORTS IN THIS FILE
"""
DEFAULT_ROUTE = '/'  # Корневое значение, когда пользователь не зашёл ни в какую команду
START_ROUTE = '/start'
MENU_ROUTE = '/menu'
HELP_ROUTE = '/help'
CURRENCY_ROUTE = '/currency'
CURRENCY_GRAPH_ROUTE = '/currency_graph'
TOTEM_ROUTE = '/totem'
DIPLOMA_ROUTE = '/diploma'
FEEDBACK_ROUTE = '/feedback'
SEND_ROUTE = '/send'
DROP_PREV_ARG = 'drop-prev'
DATA_ARG = 'text'  # Вся жизнь это симуляция, бот тебя выдумал, кнопки это то же самое что и текст


# TODO: map of admin commands


class ParsedRoute:
    """
    Класс распарсенного пути.
    Состоит из двух базовых частей:

    route - путь, выглядит как /path1 или /path1/path2

    args - словарь с ключами и значениями из пути, и ключ и значение - строка
    """
    @classmethod
    def serialize(cls, route: str, args: dict) -> str:
        res = route
        if args is None or len(args) == 0:
            return res
        return res + '?' + '&&'.join(map(lambda x: f'{x}={args[x]}', args.keys()))

    def __init__(self, unparsed_route: str):
        """
        :param unparsed_route: строка вида '/route?arg1=val1&&arg2=val2'
        """
        split_by_question = list(unparsed_route.split('?'))
        split_len = len(split_by_question)
        self.route = DEFAULT_ROUTE
        self._args = dict()
        if split_len == 1:
            self.route = unparsed_route
        elif split_len == 2:
            self.route = split_by_question[0]
            self._args = {argument.split('=')[0]: argument.split('=')[1]
                          for argument in split_by_question[1].split('&&')
                          }
        else:
            # TODO: что в такой ситуации делать?
            raise Exception(f'Found more than one argument delimiter ("?") in route: {unparsed_route}')

    def __str__(self):
        return self.serialize(self.route, self._args)

    def __eq__(self, other: str):
        return self.route == other

    def get_arg(self, key):
        if self._args is None or key not in self._args:
            return None
        return self._args[key]

    def set_arg(self, key, value):
        if self._args is None:
            self._args = {key: value}
        self._args[key] = value
