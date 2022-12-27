from src.constants import BOT_TOKEN, IS_PRODUCTION, SUDO_USERS, DB_USER, DB_USER_PASSWORD, DB_HOST, DB_NAME, DB_PORT
from src.commands import Commands
import telebot
from src.logger import Logger
from src.data_source import DataSource

bot = telebot.TeleBot(BOT_TOKEN)
logger = Logger(log_level=0 if IS_PRODUCTION else 1)
database = DataSource(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_USER_PASSWORD
)


@bot.message_handler(commands=['start'])
def say_welcome(message):
    logger.v("income command: " + str(message))
    bot.send_message(message.chat.id,
                     'Здарова, скоро тут будет супер трейд стратегия от Шлеппы, '
                     'а пока - держи мой пульс '
                     'https://www.tinkoff.ru/invest/social/profile/fleppa_war_crimes_fa?utm_source=share',
                     )


@bot.message_handler(commands=['help'])
def say_help(message):
    bot.send_message(message.chat.id, 'Вряд ли я смогу тебе рассказать о том, что я умею...'
                                      'Ведь создатели ещё не придумали зачем я нужен...')


@bot.message_handler(func=lambda message: True)
def default_handler(message):
    logger.v("income message: " + str(message))
    message_author = message.from_user.id
    if message_author in SUDO_USERS:
        try:
            splitted_message = list(map(lambda el: str(el).lower(), message.text.split()))
            command = splitted_message[0]

            if command in Commands.environment.commands:
                bot.send_message(message.chat.id, f'PROD: {IS_PRODUCTION}')
            elif command in Commands.db.commands:
                bot.send_message(message.chat.id, str(database.exec(' '.join(splitted_message[1:]))))
            else:
                bot.send_message(message.chat.id, 'Кажется такой команды нет, создатель')
        except Exception as e:
            bot.send_message(message.chat.id, "Не удалось понять сообщение от sudo_user'а: " + str(message.text))
            bot.send_message(message.chat.id, str(e))
        return
    bot.send_message(message.chat.id, 'Кажется я не знаю такой команды')
