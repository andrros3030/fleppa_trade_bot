from functools import wraps
from src.logger import Logger


def execute_decorator(logger: Logger, is_from_message: bool):
    def factory(function):
        @wraps(function)
        def decorator(*args, **kwargs):
            s_to_log = f'Executing function {function.__name__} with args: {args} and kwargs: {kwargs}'
            if is_from_message:
                s_to_log += f'\nMessage details: {str(args[0])}'
            logger.v(s_to_log)
            return function(*args, **kwargs)
        return decorator
    return factory
