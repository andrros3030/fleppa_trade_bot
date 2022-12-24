from constants import BOT_TOKEN, IS_PRODUCTION, SUDO_USERS  # ,SERVICE_API_KEY,YDB_DATABASE, YDB_ENDPOINT
import telebot
from telebot import types
from logger import Logger
# from data_source import DataSource

bot = telebot.TeleBot(BOT_TOKEN)
if __name__ == '__main__':
    IS_PRODUCTION = False
    bot.remove_webhook()
logger = Logger(log_level=0 if IS_PRODUCTION else 1)
# database = DataSource(
#     ydb_endpoint=YDB_ENDPOINT,
#     ydb_database=YDB_DATABASE,
#     # access_token=SERVICE_API_KEY,
#     logger=logger
# )
logger.v('pre-start loading is complete')


# --------------------- bot ---------------------
@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    logger.v("income command: " + str(message))
    keyboard = types.ReplyKeyboardMarkup()
    inline = types.InlineKeyboardMarkup()
    keyboard.add(types.KeyboardButton(text='keyboard_button_1'))
    keyboard.add(types.KeyboardButton(text='keyboard_button_2'))
    inline.add(types.InlineKeyboardButton('inline_button_1', callback_data='smth_1'))
    inline.add(types.InlineKeyboardButton('inline_button_2', callback_data='smth_2'))
    bot.send_message(message.chat.id,
                     'Здарова, скоро тут будет супер трейд стратегия от Шлеппы, '
                     'а пока - держи мой пульс '
                     'https://www.tinkoff.ru/invest/social/profile/fleppa_war_crimes_fa?utm_source=share',
                     reply_markup=inline,
                     )


@bot.message_handler(func=lambda message: True)
def echo(message):
    logger.v("income message: " + str(message))
    message_author = message.from_user.id
    if message_author in SUDO_USERS:
        bot.send_message(message.chat.id, 'Sudo user detected ;)')
        bot.send_message(message.chat.id, str(message))
        return
    bot.send_message(message.chat.id, 'Чел я умею только скидывать свой пульс))))))))))')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    logger.v(str(call))


@bot.message_handler(content_types=['text', 'sticker'])
def get_sticker_messages(message):
    logger.v(str(message))


if __name__ == '__main__':
    logger.v('local infinity_polling is started')
    bot.infinity_polling()
# else:
#     bot.set_webhook("https://d5dsfuv2brgj4buc3uam.apigw.yandexcloud.net")
# message.from_user.id -> id of user who sent this message
# message.from_user.first_name -> first name of user who sent this message
