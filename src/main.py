import telebot

from src.constants import global_context
from src.commands import commands
from src.logger import Logger
from src.data_source import DataSource
from src.execute_decorator import message_execute_decorator
from src.routes import DEFAULT_ROUTE

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
    chat_id = message.chat.id
    message_author = message.from_user.id
    current_route = database.get_current_route(message_author)
    is_admin = database.is_admin(message_author) or message_author in global_context.SUDO_USERS
    first_word = message.text.split()[0].lower()
    if first_word[0] == '/':
        first_word = first_word[1:]
    for cmd in commands:
        if cmd.public or is_admin:
            if first_word in cmd.commands or \
                    (current_route.route == cmd.route and cmd.route != DEFAULT_ROUTE):
                return cmd.run(
                    message=message,
                    bot=bot,
                    database=database,
                    current_route=current_route,
                    is_admin=is_admin
                )
    bot.send_message(chat_id, 'Кажется я не знаю такой команды. Попробуй /help')
