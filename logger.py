class Logger:
    log_levels: dict = {
        0: True,  # This is "error" logging level
        1: False  # This is "verbose" logging level
    }
    log_level_color: dict = {
        0: '\033[95m',
        1: '\033[91m'
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
        0: 'LOGGER/VERBOSE: ',
        1: 'LOGGER/ERROR: '
    }

    def __init__(self, log_level: int = 1):
        if log_level > 0:
            self.log_levels[1] = True
        elif log_level < 0:
            self.log_levels[0] = False
        self.v(
            f"Logger set up complete, ready to log, log level: {log_level}"
        )

    def __log(self, message: str, level: int):
        if self.log_levels[level]:
            print(self.log_level_color[level] + self.log_levels_names[level] + message + '\033[0m')

    def v(self, message: str):
        self.__log(message, level=0)

    def e(self, message: str):
        self.__log(message, level=1)
