from constants import BOT_TOKEN, IS_PRODUCTION
import telebot
from telebot import types
from logger import Logger


bot = telebot.TeleBot(BOT_TOKEN)
if __name__ == '__main__':
    IS_PRODUCTION = False
    bot.remove_webhook()
logger = Logger(log_level=0 if IS_PRODUCTION else 1)


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
                     'Здарова, скоро тут будет супер трейд стратегия от Шлеппы, а пока - держи мой пульс https://www.tinkoff.ru/invest/social/profile/fleppa_war_crimes_fa?utm_source=share',
                     reply_markup=inline,
                     )


@bot.message_handler(func=lambda message: True)
def echo(message):
    logger.v("income message: " + str(message))
    bot.send_message(message.chat.id, 'Чел я умею только скидывать свой пульс))))))))))')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    logger.v(str(call))


@bot.message_handler(content_types=['text', 'sticker'])
def get_sticker_messages(message):
  logger.v(str(message))


if __name__ == '__main__':
    bot.infinity_polling()
# else:
#     bot.set_webhook("https://d5dsfuv2brgj4buc3uam.apigw.yandexcloud.net")





