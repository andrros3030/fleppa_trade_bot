from src.constants import global_context
from src.commands import Commands
import telebot
from datetime import datetime, timedelta
import requests
from src.logger import Logger
from src.data_source import DataSource



bot = telebot.TeleBot(global_context.BOT_TOKEN)
logger = Logger(is_poduction=global_context.IS_PRODUCTION)
database = DataSource(auth_context=global_context.auth_context, logger=logger)


@bot.message_handler(commands=['start'])
def say_welcome(message):
    logger.v("income command: " + str(message))
    database.save_user(str(message.from_user.id))
    bot.send_message(message.chat.id,
                     'Здарова, скоро тут будет супер трейд стратегия от Шлеппы, '
                     'а пока - держи мой пульс '
                     'https://www.tinkoff.ru/invest/social/profile/fleppa_war_crimes_fa?utm_source=share',
                     )


@bot.message_handler(commands=['help'])
def say_help(message):
    logger.v("income command: " + str(message))
    database.save_user(str(message.from_user.id))
    bot.send_message(message.chat.id, 'Вряд ли я смогу тебе рассказать о том, что я умею...'
                                      'Ведь создатели ещё не придумали зачем я нужен...')


@bot.message_handler(func=lambda message: message.text.upper() != 'MOEX')
def default_handler(message):
    logger.v("income message: " + str(message))
    database.save_user(str(message.from_user.id))
    message_author = message.from_user.id
    if database.is_admin(message_author) or message_author in global_context.SUDO_USERS:
        try:
            splitted_message = list(map(lambda el: str(el).lower(), message.text.split()))
            command = splitted_message[0]

            if command in Commands.environment.commands:
                bot.send_message(message.chat.id, str(global_context))
            elif command in Commands.db.commands:
                bot.send_message(message.chat.id, str(database.unsafe_exec(' '.join(splitted_message[1:]))))
            elif command in Commands.set_admin.commands:
                if len(splitted_message) != 2:
                    bot.send_message(message.chat.id, 'Комманда принимает на вход один аргумент - id человека, '
                                                      'назначаемого админом')
                    return
                bot.send_message(message.chat.id, str(database.set_admin(splitted_message[1])))
            else:
                bot.send_message(message.chat.id, 'Кажется такой команды нет, создатель')
        except Exception as e:
            bot.send_message(message.chat.id, "Не удалось понять сообщение от sudo_user'а: " + str(message.text))
            bot.send_message(message.chat.id, str(e))
        return
    bot.send_message(message.chat.id, 'Кажется я не знаю такой команды')


@bot.message_handler(commands=['currency'])
def currency(message):
    today = datetime.now()
    yesterday = today - timedelta(days=7)

    today, yesterday = today.strftime('%Y-%m-%d'), yesterday.strftime('%Y-%m-%d')

    response_usd = requests.get(
        f'http://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities/usd//rub.json?from={yesterday}&till={today}')
    data_usd = response_usd.json()['securities']['data']
    usd_today = data_usd[-1][-1]
    usd_change = round((data_usd[-1][-1] - data_usd[-2][-1]) / data_usd[-2][-1] * 100, 2)

    response_eur = requests.get(
        f'http://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities/eur//rub.json?from={yesterday}&till={today}')
    data_eur = response_eur.json()['securities']['data']
    eur_today = data_eur[-1][-1]
    eur_change = round((data_eur[-1][-1] - data_eur[-2][-1]) / data_eur[-2][-1] * 100, 2)

    result = []

    if usd_change < 0:
        result.append(f'USD: {usd_today} (-{usd_change} % 🔴)')
    elif usd_change > 0:
        result.append(f'USD: {usd_today} (+{usd_change} % 🟢)')
    else:
        result.append(f'USD: {usd_today} ({usd_change} % ⚪)')

    if eur_change < 0:
        result.append(f'EUR: {eur_today} (-{eur_change} % 🔴)')
    elif eur_change > 0:
        result.append(f'EUR: {eur_today} (+{eur_change} % 🟢)')
    else:
        result.append(f'EUR: {eur_today} ({eur_change} % ⚪)')

    bot.send_message(message.chat.id, '\n'.join(result))

