"""
DO NOT IMPORT BASE_MODULES, OTHER FEATURES OR ROOT MODULES EXCEPT CONTEXT
"""
from src.context import CallContext
from src.common_modules.request_currency import currency_info
from src.common_modules.drawer import currency_plot, currency_data
from src.common_modules.homiak_diploma import diploma


# TODO: !!!!!!!!!!!!ОБРАБОТКА ОШИБОК!!!!!!!!


def get_totem(cc: CallContext):
    cc.bot.send_message(cc.chat_id, str(cc.totem))
    cc.bot.send_message(cc.chat_id, "Давай я выдам тебе диплом, "
                                    "которым ты сможешь поделиться со своими друзьями хомячками? "
                                    "Жми /diploma")


def say_wellcome(cc: CallContext):
    start_link = cc.splitted_message[1] if len(cc.splitted_message) > 1 else None
    cc.database.save_user(user_id=cc.message_author, involve_link=start_link)
    cc.bot.send_message(cc.chat_id, cc.database.get_start_message(start_link=start_link))


def currency(cc: CallContext):
    currency_tickers = ['USD', 'EUR']
    info = currency_info(currency_tickers)
    result = []
    for i in currency_tickers:
        result.append(info[i]['full_info'])

    cc.bot.send_message(cc.chat_id, '\n'.join(result))


def get_diploma(cc: CallContext):
    lastname = cc.user_data.last_name
    if lastname is None:
        lastname = ""
    else:
        lastname = " " + lastname
    cc.bot.send_photo(cc.chat_id, photo=diploma(cc.user_data.first_name + lastname))


def currency_graph(cc: CallContext):
    currency_tickers = ['USD', 'EUR']
    for i in currency_tickers:
        curr = currency_data(i)
        cc.bot.send_photo(cc.chat_id, photo=currency_plot(curr[0], curr[1], i), caption=f'Вот тебе график {i}/RUB')


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
