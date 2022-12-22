from constants import BOT_TOKEN
import telebot


bot = telebot.TeleBot(BOT_TOKEN)


# --------------------- bot ---------------------
@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    bot.send_message(message.chat.id,
                     'Здарова, скоро тут будет супер трейд стратегия от Шлеппы, а пока - держи мой пульс https://www.tinkoff.ru/invest/social/profile/fleppa_war_crimes_fa?utm_source=share')


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, 'Чел я умею только скидывать свой пульс))))))))))')
