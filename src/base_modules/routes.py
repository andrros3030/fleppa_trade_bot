"""
В этом файле описана логика работы с путями, которые мы храним для каждого пользователя
NO PROJECT IMPORTS IN THIS FILE
"""
DEFAULT_ROUTE = '/'  # Корневое значение, когда пользователь не зашёл ни в какуб команду


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
        if split_len == 0:
            self.route = DEFAULT_ROUTE
        elif split_len == 1:
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
        res = f'{self.route}'
        if self.args is None:
            return res
        return res + '?' + '&&'.join(map(lambda x, y: f'{x}={y}', self.args.items()))
