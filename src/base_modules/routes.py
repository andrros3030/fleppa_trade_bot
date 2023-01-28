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
# TODO: map of admin commands


class ParsedRoute:
    """
    Класс распарсенного пути.
    Состоит из двух базовых частей:

    route - путь, выглядит как /path1 или /path1/path2

    args - словарь с ключами и значениями из пути, и ключ и значение - строка
    """
    def __init__(self, unparsed_route: str):
        """
        :param unparsed_route: строка вида '/route?arg1=val1&&arg2=val2'
        """
        split_by_question = list(unparsed_route.split('?'))
        split_len = len(split_by_question)
        self.route = DEFAULT_ROUTE
        self.args = dict()
        if split_len == 1:
            self.route = unparsed_route
        elif split_len == 2:
            self.route = split_by_question[0]
            self.args = {argument.split('=')[0]: argument.split('=')[1]
                         for argument in split_by_question[1].split('&&')
                         }
        else:
            # TODO: что в такой ситуации делать?
            raise Exception(f'Found more than one argument delimiter ("?") in route: {unparsed_route}')

    def __str__(self):
        res = self.route
        if self.args is None or len(self.args) == 0:
            return res
        return res + '?' + '&&'.join(map(lambda x: f'{x}={self.args[x]}', self.args.keys()))

    def __eq__(self, other: str):
        return self.route == other
