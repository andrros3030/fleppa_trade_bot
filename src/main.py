from src.constants import global_context
from src.commands import Commands
import telebot
from src.logger import Logger
from src.data_source import DataSource

bot = telebot.TeleBot(global_context.BOT_TOKEN)
logger = Logger(is_poduction=global_context.IS_PRODUCTION)


@bot.message_handler(commands=['start'])
def say_welcome(message):
    logger.v("income command: " + str(message))
    database = DataSource(auth_context=global_context.auth_context, logger=logger)
    database.save_user(str(message.from_user.id))
    bot.send_message(message.chat.id,
                     'Здарова, скоро тут будет супер трейд стратегия от Шлеппы, '
                     'а пока - держи мой пульс '
                     'https://www.tinkoff.ru/invest/social/profile/fleppa_war_crimes_fa?utm_source=share',
                     )


@bot.message_handler(commands=['help'])
def say_help(message):
    logger.v("income command: " + str(message))
    database = DataSource(auth_context=global_context.auth_context, logger=logger)
    database.save_user(str(message.from_user.id))
    bot.send_message(message.chat.id, 'Вряд ли я смогу тебе рассказать о том, что я умею...'
                                      'Ведь создатели ещё не придумали зачем я нужен...')


@bot.message_handler(func=lambda message: True)
def default_handler(message):
    logger.v("income message: " + str(message))
    database = DataSource(auth_context=global_context.auth_context, logger=logger)
    database.save_user(str(message.from_user.id))
    message_author = message.from_user.id
    if message_author in global_context.SUDO_USERS:
        try:
            splitted_message = list(map(lambda el: str(el).lower(), message.text.split()))
            command = splitted_message[0]

            if command in Commands.environment.commands:
                bot.send_message(message.chat.id, str(global_context))
            elif command in Commands.db.commands:
                database = DataSource(auth_context=global_context.auth_context, logger=logger)
                bot.send_message(message.chat.id, str(database.unsafe_exec(' '.join(splitted_message[1:]))))
            else:
                bot.send_message(message.chat.id, 'Кажется такой команды нет, создатель')
        except Exception as e:
            bot.send_message(message.chat.id, "Не удалось понять сообщение от sudo_user'а: " + str(message.text))
            bot.send_message(message.chat.id, str(e))
        return
    bot.send_message(message.chat.id, 'Кажется я не знаю такой команды')
