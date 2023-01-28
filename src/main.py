"""
THIS FILE IS A TRANSITION POINT FOR ALL COMMANDS
DO NOT IMPORT FEATURES HERE
"""
import telebot

from src.context import global_context
from src.commands import commands
from src.base_modules.logger import Logger
from src.base_modules.routes import DEFAULT_ROUTE, ParsedRoute
from src.common_modules.data_source import DataSource
from src.common_modules.execute_decorator import message_execute_decorator
from src.common_modules.custom_sender import send_long_message

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
                send_long_message(bot, admin, error_data)
            except Exception as e:
                logger.e(f"FATAL: can't send error message to admin, causing error: {str(e)}"
                         f'\nError to send: {error_data}')
    else:
        send_long_message(bot, message.chat.id, error_data)


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
    has_text = False
    lower_message = None
    first_word = None
    if message.text is not None:
        lower_message = message.text.lower()
        first_word = lower_message.split()[0]
        if first_word[0] == '/':
            first_word = first_word[1:]
        has_text = True
    logger.i(f"message_author: {message_author} current route: {current_route}; "
             f"first_word: {first_word}; lower_message: {lower_message}")
    for cmd in commands:
        if cmd.public or is_admin:
            # TODO: сделать предсказумую логику для взаимодействия с командами по путям
            # возможно придется написать обработчик посложнее для проверки сигнатуры команды
            if (has_text and (first_word in cmd.commands or lower_message in cmd.commands)) or \
                    (current_route.route == cmd.route and cmd.route != DEFAULT_ROUTE):
                return cmd.run(
                    message=message,
                    bot=bot,
                    database=database,
                    current_route=current_route,
                    is_admin=is_admin,
                    logger=logger
                )
    return bot.send_message(chat_id, 'Кажется я не знаю такой команды. Попробуй /help')


@bot.callback_query_handler(func=lambda query: True)
def callback_handler(query):
    if query.data is not None:
        base_func_route = ParsedRoute(query.data)
        query_author = query.from_user.id
        is_admin = database.is_admin(query_author) or query_author in global_context.SUDO_USERS
        current_route = database.get_current_route(query_author)
        logger.i(f'query_author: {query_author} base_func_route: {base_func_route}')
        for cmd in commands:
            if cmd.public or is_admin:
                if base_func_route.route == cmd.route:
                    return cmd.run(
                        query=query,
                        bot=bot,
                        database=database,
                        current_route=current_route,
                        is_admin=is_admin,
                        logger=logger
                    )
