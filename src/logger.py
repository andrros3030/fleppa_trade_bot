def yellow_color():
    return '\033[93m'


def pink_color():
    return '\033[95m'


def light_blue_color():
    return '\033[96m'


def red_color():
    return '\033[91m'


def dark_green_color():
    return '\033[92m'


def dark_blue_color():
    return '\033[94m'


class Logger:
    log_levels: dict = {
        0: True,  # This is "error" logging level
        1: False,  # This is "warning" logging level
        2: False,  # This is "info" logging level
        3: False  # This is "verbose" logging level
    }
    log_level_color: dict = {
        0: red_color(),
        1: pink_color(),
        2: light_blue_color(),
        3: dark_blue_color(),
        # HEADER = '\033[95m'
        # OKCYAN = '\033[96m'
        # BOLD = '\033[1m'
        # UNDERLINE = '\033[4m'
    }
    log_levels_names: dict = {
        0: 'LOGGER/ERROR:   ',
        1: 'LOGGER/WARNING: ',
        2: 'LOGGER/INFO:    ',
        3: 'LOGGER/VERBOSE: ',
    }

    def __init__(self, is_poduction: bool, base_func=print):
        self.is_production = is_poduction
        self.base_func = base_func
        if not is_poduction:
            self.log_levels[1] = True
            self.log_levels[2] = True
            self.log_levels[3] = True
        self.v(
            f"Logger set up complete, ready to log, prod: {is_poduction}"
        )

    def __log(self, message: str, level: int, override_color: str = None):
        real_color = override_color if override_color is not None else self.log_level_color[level]
        end_char = '\r' if self.is_production else '\n'
        replace_char = '\n' if self.is_production else '\r'
        message = str(message).replace(replace_char, end_char)
        if self.log_levels[level]:
            return self.base_func(real_color + self.log_levels_names[level] + message + '\033[0m', end=end_char)

    def v(self, message: str, override_color: str = None):
        return self.__log(message, level=3, override_color=override_color)

    def i(self, message: str, override_color: str = None):
        return self.__log(message, level=2, override_color=override_color)

    def w(self, message: str, override_color: str = None):
        return self.__log(message, level=1, override_color=override_color)

    def e(self, message: str, override_color: str = None):
        return self.__log(message, level=0,  override_color=override_color)
