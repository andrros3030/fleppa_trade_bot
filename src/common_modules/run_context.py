"""
Контекст запуска, достаёт из окружения нужные переменные для работы бота
Формирует авторизационный контекст для базы данных
ONLY BASE AND COMMON MODULES ALLOWED TO BE IMPORTED
"""
import os
import subprocess
import json
from src.base_modules.db_auth_context import DBAuthContext


context_url = "169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"


def _mask_token(token: str):
    """
    Функция для маскировки секретов

    :param token: строка, которую необходимо заблюрить

    :returns: безопасное представление секрета
    """
    if token is None:
        return 'None'
    if type(token) is not str:
        token = str(token)
    if len(token) < 10:
        return '*'.join(token[::2])
    return token[0:4] + '*' * (len(token) - 5)


def _mask_tokens(tokens: dict or None) -> str:
    if tokens is None:
        return ''
    result = []
    for key, value in tokens.items():
        result.append(f'{key}: {_mask_token(value)}')
    return '\n'.join(result)


class Context:
    """
    Контекст вызова функции веб-хука или локального запуска бота
    """

    def __init__(self):
        """
        Получение из переменных среды необходимых секретов для подключения ко всем службам
        """
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_PORT = os.getenv('DB_PORT')
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')
        self.BOT_TOKEN = os.getenv('BOT_TOKEN')
        self.WEBHOOK = os.getenv('WEBHOOK')
        self.BUILD_DATE = os.getenv('BUILD_DATE')
        self.IMAGE = os.getenv('IMAGE')
        self.IS_PRODUCTION = True
        self.SUDO_USERS = [
            439133935,  # Андрей
        ]
        self.FEEDBACK_CHAT_ID = [
            -898292404,  # Фидбэчница
        ]
        self.context = None
        self.db_auth_context = DBAuthContext(
            on_error=self.set_context_from_env
        )

    def set_testing_mode(self):
        """
        Установка тестового окружения. Если эта функция не была вызвана
        после инициализации контекста - окружение является продовым
        """
        # TODO: replace environment variables values here
        self.IS_PRODUCTION = False
        self._update_db_context()

    def set_context_from_env(self):
        """
        Установка контекста запуска из ВМ, работает в продакшен окружении Compute Cloud.
        Получает контекст из внутренней ручки YC с помощью запроса через bash.
        """
        if not self.IS_PRODUCTION:
            # Если окружение не продакшен - выполнение команды не доступно
            return
        bash_command = f'curl -H Metadata-Flavor:Google {context_url}'
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if output is not None:
            # TODO: обработать ошибки и шедулить обновление контекста, когда токен сыреет
            self.context = json.loads(output)
        self._update_db_context()

    def set_context(self, new_context):
        """
        Установка контекста запуска функции, работает только в продакшен окружении Cloud Functions

        :param new_context: контекст запуска Yandex Cloud Functions
        """
        self.context = new_context
        self._update_db_context()

    def _update_db_context(self):
        self.db_auth_context.fill(
            user=self.DB_USER,
            password=self.context["access_token"] if self.IS_PRODUCTION else self.DB_USER_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            is_prod=self.IS_PRODUCTION,
            dbname=self.DB_NAME,
        )

    def __str__(self):
        """
        Текстовое представление основных параметров контекста запуска

        :return: строка, разделенная \n
        """
        # TODO: сделать для self.context подробный вывод
        token = self.context["access_token"] if self.IS_PRODUCTION else self.DB_USER_PASSWORD
        return f"PROD: {self.IS_PRODUCTION}\n" \
               f"BUILD_DATE: {self.BUILD_DATE}\n" \
               f"IMAGE: {self.IMAGE}\n" \
               f"{_mask_tokens(self.context)}\n" \
               f"DB_TOKEN: {_mask_token(token)}"


# TODO: тех долг, откзаться от глобальной переменной в пользу DI
global_context = Context()
