"""
DO NOT IMPORT BASE_MODULES, OTHER FEATURES OR ROOT MODULES EXCEPT CONTEXT
"""
from src.context import global_context, CallContext
from src.common_modules.request_currency import currency_info
from src.common_modules.drawer import currency_plot, currency_data
from src.common_modules.homiak_diploma import diploma
from src.common_modules.photoshop import add_fleppa_wm
from telebot.types import InlineKeyboardButton


# TODO: !!!!!!!!!!!!ОБРАБОТКА ОШИБОК!!!!!!!!


def get_totem(cc: CallContext):
    cc.bot.send_message(cc.chat_id, str(cc.totem), reply_markup=cc.reply_markup)


def feedback(cc: CallContext):
    if cc.current_route.route != cc.base_route:
        cc.logger.i(f'feedback for {cc.message_author} started')
        if cc.database.is_banned(cc.message_author):
            cc.bot.send_message(cc.chat_id, 'Отправка фидбэка недоступна')
            return
        cc.database.set_route(cc.message_author, route=cc.base_route)
        cc.bot.send_message(cc.chat_id, 'Пожалуйста, отправьте свой фид-бэк о работе бота. '
                                        'Вы можете добавить фото или видео, админы посмотрят их и вернутся в чат',
                            reply_markup=cc.reply_markup)
    else:
        for feedback_chat in global_context.FEEDBACK_CHAT_ID:
            res = cc.bot.forward_message(feedback_chat, cc.chat_id, cc.message_id)
            cc.database.save_feedback_origin(
                user_id=cc.message_author,
                origin_message_id=cc.message_id,
                forwarded_message_id=res.message_id
            )
        cc.bot.send_message(cc.chat_id, reply_to_message_id=cc.message_id, text='Фид-бэк отправлен админам, спасибо',
                            reply_markup=cc.reply_markup)
        cc.database.set_route(cc.message_author)


def say_welcome(cc: CallContext):
    start_link = cc.splitted_message[1] if len(cc.splitted_message) > 1 else None
    cc.database.save_user(user_id=cc.message_author, involve_link=start_link)
    cc.bot.send_message(cc.chat_id, cc.database.get_start_message(start_link=start_link), reply_markup=cc.reply_markup)


def currency(cc: CallContext):
    currency_tickers = ['USD', 'EUR', 'CNY']
    info = currency_info(currency_tickers)
    result = [f'Курсы от {info["trade_day"]} {info["request_time"]} '
              f'(изменение к закрытию {info["trade_date_before"]})', '']
    for i in currency_tickers:
        result.append(info[i]['full_info'])
    cc.reply_markup.add(InlineKeyboardButton(
        text='Построить график',
        callback_data=f'/currency_graph?currencies={";".join(currency_tickers)}')
    )
    cc.bot.send_message(cc.chat_id, '\n'.join(result), reply_markup=cc.reply_markup)


def get_diploma(cc: CallContext):
    lastname = cc.user_data.last_name
    if lastname is None:
        lastname = ""
    else:
        lastname = " " + lastname
    cc.bot.send_photo(cc.chat_id, photo=add_fleppa_wm(diploma(cc.user_data.first_name + lastname, cc.totem.totem),
                                                      x=397, y=1584),
                      caption='Похвастайся друзьям дипломом и узнай, кто они на бирже 😱', reply_markup=cc.reply_markup)


def currency_graph(cc: CallContext):
    currency_tickers = ['USD', 'EUR']
    for i in currency_tickers:
        curr = currency_data(i)
        cc.bot.send_photo(cc.chat_id, photo=add_fleppa_wm(currency_plot(curr[0], curr[1], i), 100, 50),
                          caption=f'Вот тебе график {i}/RUB')
    cc.bot.send_message(cc.chat_id, 'Если ты знаешь, как сделать этот график лучше — оставь свой отзыв, '
                                    'вызвав команду /feedback', reply_markup=cc.reply_markup)


def menu(cc: CallContext):
    return cc.bot.send_message(cc.chat_id, "Какой-то текст для менюшки", reply_markup=cc.reply_markup)

# Пример работы команды из двух сообщений
# def command_name(cc: CallContext):
#     if cc.current_route.route != cc.base_route:  # проверяем, что путь не является базовым для этой команды
#         # do smth
#         cc.database.set_route(
#             cc.message_author,
#             route=cc.base_route
#         )  # сохранили информацию, что пользователь вошел в эту команду
#     else:
#         # выполняем второе действие
#         cc.database.set_route(cc.message_author)  # НЕ ЗАБЫВАЕМ ОБНУЛИТЬ ПУТЬ


# Пример работы команды из трёх и более сообщений
# def command_name(cc: CallContext):
#     if cc.current_route.route != cc.base_route:  # проверяем, что путь не является базовым для этой команды
#         # do smth
#         cc.database.set_route(
#             cc.message_author,
#             route=cc.base_route
#         )  # сохранили информацию, что пользователь вошел в эту команду
#     else:
#         if cc.current_route.args is None:  # проверяем, что аргументов у пути пока нет
#             # do smth
#             cc.current_route.args = {'arg1': 'some_value'}
#             cc.database.set_route(cc.message_author, str(cc.current_route))
#         else:  # если аргумент у пути уже есть
#             # выполняем третье действие или делаем еще одно ветвление
#             cc.database.set_route(cc.message_author)  # НЕ ЗАБЫВАЕМ ОБНУЛИТЬ ПУТЬ
