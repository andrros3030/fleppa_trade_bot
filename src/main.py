from src.constants import global_context
from src.commands import Commands
import telebot
from src.logger import Logger
from src.data_source import DataSource
from src.execute_decorator import message_execute_decorator

bot = telebot.TeleBot(global_context.BOT_TOKEN)


def error_handler(message, error):
    error_data = f'Catched error in decorator: {str(error)}' \
                 f'\nUser: {str(message.from_user.id)}' \
                 f'\nJSON: {str(message)}'
    logger.w(error_data)
    bot.send_message(message.chat.id, 'Необработанное исключение в работе бота. '
                                      'Админы уже получили информацию об ошибке, но мы будем очень признательны, '
                                      'если ты расскажешь, какая команда вызвала ошибку с помощью /feedback')
    for admin in global_context.SUDO_USERS:
        try:
            bot.send_message(admin, error_data)
        except Exception as e:
            logger.e(f"FATAL: can't send error message to admin, causing error: {str(e)}"
                     f'\nError to send: {error_data}')


logger = Logger(is_poduction=global_context.IS_PRODUCTION)
database = DataSource(auth_context=global_context.auth_context, logger=logger)
msg_executor = message_execute_decorator(logger=logger, on_error=error_handler)


@bot.message_handler(commands=['feedback'], chat_types=['private'])
@msg_executor
def start_feedback(message):
    return Commands.feedback.run(
        message=message,
        bot=bot,
        database=database,
        current_route='/'
    )


@bot.message_handler(commands=['reply'])
@msg_executor
def start_reply(message):
    return Commands.reply.run(
        message=message,
        bot=bot,
        database=database,
        current_route='/'
    )


@bot.message_handler(commands=['start'], chat_types=['private'])
@msg_executor
def say_welcome(message):
    message_content = list(message.text.split())
    start_link = message_content[1] if len(message_content) > 1 else None
    database.save_user(user_id=str(message.from_user.id), involve_link=start_link)
    bot.send_message(message.chat.id, database.get_start_message(start_link=start_link))


@bot.message_handler(commands=['help'])
@msg_executor
def say_help(message):
    bot.send_message(message.chat.id, 'Вряд ли я смогу тебе рассказать о том, что я умею...'
                                      'Ведь создатели ещё не придумали зачем я нужен...')


@bot.message_handler(commands=['crash'])
@msg_executor
def do_crash(message):
    message_author = message.from_user.id
    if database.is_admin(message_author) or message_author in global_context.SUDO_USERS:
        bot.send_message(message.chat.id, 'Крашаюсь, проверяй')
        raise Exception('Краш вызван специально')


@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                               'text', 'location', 'contact', 'sticker'])
@msg_executor
def absolutely_all_handler(message):
    chat_id = message.chat.id
    message_author = message.from_user.id
    current_route = database.get_current_route(message_author)
    if current_route.route == Commands.feedback.route:
        return Commands.feedback.run(
            message=message,
            bot=bot,
            database=database,
            current_route=current_route
        )
    if current_route.route == Commands.reply.route:
        return Commands.reply.run(
            message=message,
            bot=bot,
            database=database,
            current_route=current_route
        )
    if database.is_admin(message_author) or message_author in global_context.SUDO_USERS:
        try:
            splitted_message = list(map(lambda el: str(el).lower(), message.text.split()))
            command = splitted_message[0]

            if command in Commands.environment.commands:
                Commands.environment.run(
                    message, bot, database, current_route
                )
            elif command in Commands.db.commands:
                Commands.db.run(
                    message, bot, database, current_route
                )
            elif command in Commands.set_admin.commands:
                Commands.set_admin.run(
                    message, bot, database, current_route
                )
            elif command in Commands.generate_link.commands:
                Commands.generate_link.run(
                    message, bot, database, current_route
                )
            else:
                bot.send_message(chat_id, 'Кажется такой команды нет, создатель')
        except Exception as e:
            bot.send_message(chat_id, "Не удалось понять сообщение от sudo_user'а: " + str(message.text))
            bot.send_message(chat_id, str(e))
        return
    bot.send_message(chat_id, 'Кажется я не знаю такой команды')
