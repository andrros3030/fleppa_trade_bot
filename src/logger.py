def error_color():
    return '\033[95m'


def verbose_color():
    return '\033[96m'


def pink_color():
    return '\033[91m'


def green_color():
    return '\033[92m'


def blue_color():
    return '\033[94m'


class Logger:
    log_levels: dict = {
        0: True,  # This is "error" logging level
        1: False  # This is "verbose" logging level
    }
    log_level_color: dict = {
        0: error_color(),
        1: verbose_color(),
        # HEADER = '\033[95m'
        # OKBLUE = '\033[94m'
        # OKCYAN = '\033[96m'
        # OKGREEN = '\033[92m'
        # WARNING = '\033[93m'
        # FAIL = '\033[91m'
        # ENDC = '\033[0m'
        # BOLD = '\033[1m'
        # UNDERLINE = '\033[4m'
    }
    log_levels_names: dict = {
        0: 'LOGGER/ERROR: ',
        1: 'LOGGER/VERBOSE: '
    }

    def __init__(self, is_poduction: bool):
        self.is_production = is_poduction
        if not is_poduction:
            self.log_levels[1] = True
        self.v(
            f"Logger set up complete, ready to log, prod: {is_poduction}"
        )

    def __log(self, message: str, level: int, override_color: str = None):
        real_color = override_color if override_color is not None else self.log_level_color[level]
        end_char = '\r' if self.is_production else '\n'
        if self.log_levels[level]:
            print(real_color + self.log_levels_names[level] + str(message) + '\033[0m', end=end_char)

    def v(self, message: str, override_color: str = None):
        self.__log(message, level=1, override_color=override_color)

    def e(self, message: str, override_color: str = None):
        self.__log(message, level=0,  override_color=override_color)
