from src.constants import BOT_TOKEN, IS_PRODUCTION, SUDO_USERS
import telebot
from src.logger import Logger

bot = telebot.TeleBot(BOT_TOKEN)
logger = Logger(log_level=0 if IS_PRODUCTION else 1)


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
            real_command = list(map(lambda el: str(el).lower(), message.text.split()))
            if real_command[0] in ['env', 'prod', 'environment', 'среда']:
                bot.send_message(message.chat.id, f'PROD: {IS_PRODUCTION}')
            else:
                bot.send_message(message.chat.id, 'Кажется такой команды нет, создатель')
        except Exception as e:
            bot.send_message(message.chat.id, "Не удалось понять сообщение от sudo_user'а: " + str(message.text))
            bot.send_message(message.chat.id, str(e))
        return
    bot.send_message(message.chat.id, 'Кажется я не знаю такой команды')
