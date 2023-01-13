from src.constants import global_context
from src.commands import Commands
import telebot
from src.logger import Logger
from src.data_source import DataSource
from src.execute_decorator import message_execute_decorator

bot = telebot.TeleBot(global_context.BOT_TOKEN)


def error_handler(message, error):
    bot.send_message(message.chat.id, 'FATAL ERROR')  # TODO: прописать текстовку
    for admin in global_context.SUDO_USERS:
        bot.send_message(admin, f'Catched error in decorator: {str(error)}'
                                f'\nUser: {str(message.from_user.id)}'
                                f'\nJSON: {str(message)}')


logger = Logger(is_poduction=global_context.IS_PRODUCTION)
database = DataSource(auth_context=global_context.auth_context, logger=logger)
msg_executor = message_execute_decorator(logger=logger, on_error=error_handler)


@bot.message_handler(commands=['start'])
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
def say_help(message):
    bot.send_message(message.chat.id, 'Крашаюсь, проверяй')
    raise Exception('Краш вызван специально')


@bot.message_handler(func=lambda message: True)
@msg_executor
def default_handler(message):
    chat_id = message.chat.id
    message_author = message.from_user.id
    if database.is_admin(message_author) or message_author in global_context.SUDO_USERS:
        try:
            splitted_message = list(map(lambda el: str(el).lower(), message.text.split()))
            command = splitted_message[0]

            if command in Commands.environment.commands:
                bot.send_message(chat_id, str(global_context))
            elif command in Commands.db.commands:
                bot.send_message(chat_id, str(database.unsafe_exec(' '.join(splitted_message[1:]))))
            elif command in Commands.set_admin.commands:
                if len(splitted_message) != 2:
                    bot.send_message(chat_id, 'Комманда принимает на вход один аргумент - id человека, '
                                              'назначаемого админом')
                    return
                bot.send_message(chat_id, str(database.set_admin(splitted_message[1])))
            elif command in Commands.generate_link.commands:
                if len(splitted_message) < 2:
                    bot.send_message(chat_id, 'Введите описание создаваемой ссылки и, '
                                              'если необходимо, стартовое сообщение через ;')
                    return
                content = ' '.join(splitted_message[1:])
                desc = content.split(';')[0]
                sm = content.split(';')[1] if len(content.split(';')) > 1 else None
                link = database.generate_link(description=desc, startup_message=sm)
                bot.send_message(chat_id, 't.me/' + bot.get_me().username + '?start=' + link)
            else:
                bot.send_message(chat_id, 'Кажется такой команды нет, создатель')
        except Exception as e:
            bot.send_message(chat_id, "Не удалось понять сообщение от sudo_user'а: " + str(message.text))
            bot.send_message(chat_id, str(e))
        return
    bot.send_message(chat_id, 'Кажется я не знаю такой команды')
