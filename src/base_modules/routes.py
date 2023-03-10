"""
В этом файле описана логика работы с путями, которые мы храним для каждого пользователя
+ константные пути для команд
NO PROJECT IMPORTS IN THIS FILE
"""
from typing import List
from urllib.parse import urlparse, urlencode, parse_qs


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
        return route + '?' + urlencode(query=args, doseq=True)
        # res = route
        # if args is None or len(args) == 0:
        #     return res
        # return res + '?' + '&'.join(map(lambda x: '%s=%s' % (x, args[x]), args.keys()))

    def __init__(self, unparsed_route: str):
        """
        :param unparsed_route: строка вида '/route?arg1=val1&arg2=val2'
        """
        parse_result = urlparse(unparsed_route)
        self.route = parse_result.path
        self._args = dict(parse_qs(parse_result.query))  # функция спокойно парсит всё, кроме &

    def __str__(self):
        return self.serialize(self.route, self._args)

    def __eq__(self, other: str):
        return self.route == other

    def get_arg(self, key) -> List[str] or None:
        """
        :param key: ключ параметра
        :return: СПИСОК параметров
        """
        if self._args is None or key not in self._args:
            return None
        return self._args[key]

    def set_arg(self, key, value):
        if self._args is None:
            self._args = {key: value}
        self._args[key] = value
