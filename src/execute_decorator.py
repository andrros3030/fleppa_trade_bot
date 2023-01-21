"""
В этом файле описан декоратор для функций, работающих при вызове бота
"""
from functools import wraps
from src.logger import Logger


def message_execute_decorator(logger: Logger, on_error):
    """
    Функция-декоратор для обертки выполняемых функций. Логгирует запуск функции с её аргументами (сообщением)

    :param logger: объект для записи логов

    :param on_error: функция, вызываемая при ошибке в ходе выполнения декорируемой функции
    (сигнатура: telebot.types.Message, Exception)
    """
    def factory(function):
        """
        Обёртка над декоратором для того, чтобы передавать в него функцию

        :param function: функция, выполняемая декоратором
        """
        @wraps(function)
        def decorator(message):
            """
            Декоратор для сообщений. Логирует и реализует безопасный запуск через try-catch

            :param message: сообщение прилетающее в бота (telebot.types.Message)
            """
            s_to_log = f'Executing function {function.__name__} with args: {message} and kwargs: {message}'
            s_to_log += f'\nMessage details: {str(message)}'
            logger.v(s_to_log)
            try:
                return function(message)
            except Exception as e:
                on_error(message, e)
        return decorator
    return factory
