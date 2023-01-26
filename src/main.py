"""
THIS FILE IS A TRANSITION POINT FOR ALL COMMANDS
DO NOT IMPORT FEATURES HERE
"""
import telebot

from src.context import global_context
from src.commands import commands
from src.base_modules.logger import Logger
from src.base_modules.routes import DEFAULT_ROUTE
from src.common_modules.data_source import DataSource
from src.common_modules.execute_decorator import message_execute_decorator

bot = telebot.TeleBot(global_context.BOT_TOKEN)
logger = Logger(is_poduction=global_context.IS_PRODUCTION)
database = DataSource(auth_context=global_context.auth_context, logger=logger)


def error_handler(message, error):
    error_data = f'Catched error in decorator: {str(error)}' \
                 f'\nUser: {str(message.from_user.id)}' \
                 f'\nJSON: {str(message)}'
    logger.w(error_data)
    if global_context.IS_PRODUCTION:
        bot.send_message(message.chat.id, 'Необработанное исключение в работе бота. '
                                          'Админы уже получили информацию об ошибке, но мы будем очень признательны, '
                                          'если ты расскажешь, какая команда вызвала ошибку с помощью /feedback')
        for admin in global_context.SUDO_USERS:
            try:
                bot.send_message(admin, error_data)
            except Exception as e:
                logger.e(f"FATAL: can't send error message to admin, causing error: {str(e)}"
                         f'\nError to send: {error_data}')
    else:
        bot.send_message(message.chat.id, error_data)


msg_executor = message_execute_decorator(logger=logger, on_error=error_handler)


@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                               'text', 'location', 'contact', 'sticker'])
@msg_executor
def absolutely_all_handler(message):
    """
    Агрегатор всех сообщений. Подбирает доступную команду пользователю для заданного сообщения и текущего пути.

    :param message: сообщение, триггер функции

    :return: результат выполнения команды
    """
    chat_id = message.chat.id
    message_author = message.from_user.id
    current_route = database.get_current_route(message_author)
    is_admin = database.is_admin(message_author) or message_author in global_context.SUDO_USERS
    lower_message = message.text.lower()
    first_word = lower_message.split()[0]
    if first_word[0] == '/':
        first_word = first_word[1:]
    should_run = None  # Команда, которую следует запустить по причине нахождения в её директории
    may_run = None  # Команда, которую можно запустить по причине совпадения псевдонима и текста пользователя
    for cmd in commands:
        if cmd.public or is_admin:
            if current_route.route == cmd.route and cmd.route != DEFAULT_ROUTE:
                should_run = cmd
            if first_word in cmd.commands or lower_message in cmd.commands:
                may_run = cmd
    if should_run is not None:
        """
        Если пользователь находится в директории одной из команд
        - запускаем внутреннюю команду для этой команды
        """
        return should_run.run(
                    message=message,
                    bot=bot,
                    database=database,
                    current_route=current_route,
                    is_admin=is_admin,
                    logger=logger,
                    is_inner=True
                )
    elif may_run is not None:
        """
        Если пользователь в данный момент не находится в директории какой-либо команды 
        - мы запускаем команду с совпадением по псевдониму
        """
        return may_run.run(
                    message=message,
                    bot=bot,
                    database=database,
                    current_route=current_route,
                    is_admin=is_admin,
                    logger=logger
                )
    """
    Иначе, если не удалось подобрать команду по псевдониму и пользователь в корневой директории - выводим вот это 
    """
    return bot.send_message(chat_id, 'Кажется я не знаю такой команды. Попробуй /help')
