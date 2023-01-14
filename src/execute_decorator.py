from functools import wraps
from src.logger import Logger


# TODO: написать документацию к методу и его аргументам
def message_execute_decorator(logger: Logger, on_error):
    def factory(function):
        @wraps(function)
        def decorator(message):
            s_to_log = f'Executing function {function.__name__} with args: {message} and kwargs: {message}'
            s_to_log += f'\nMessage details: {str(message)}'
            logger.v(s_to_log)
            try:
                return function(message)
            except Exception as e:
                on_error(message, e)
        return decorator
    return factory
