"""
DO NOT IMPORT BASE_MODULES, OTHER FEATURES OR ROOT MODULES EXCEPT CONTEXT
"""
from src.context import CallContext
from src.base_modules.constants import AVAILABLE_CURRENCY
from src.common_modules.request_currency import currency_info
from src.common_modules.drawer import currency_plot, currency_data
from src.common_modules.photoshop import add_fleppa_wm
from src.common_modules.markups import back_transition, markup_transitions, currency_graph_transition, currency_options


# TODO: получается, что любая функция имеет свой route, а большинство бизнесовых не выполняются за одной действие
def match_ticker(user_query):
    """
    Подбор соответствующего тикера для пользовательского запроса
    Сейчас закостылен под валюты

    :param user_query: пользовательский ввод

    :return: тикер или None
    """
    user_query = user_query.lower()
    for key in AVAILABLE_CURRENCY:
        if user_query == key or user_query in AVAILABLE_CURRENCY[key]:
            return key
    return None


def match_many_tickers(user_query):
    tickers = str(user_query).split(';')
    return set(match_ticker(el) for el in tickers)


def currency(cc: CallContext):
    if cc.trigger_by_command and cc.triggered_without_param:
        cc.database.set_route(user_id=cc.message_author, route=cc.base_route)
        cc.bot.send_message(cc.chat_id, text="Выбери нужную валюту",
                            reply_markup=markup_transitions(currency_options(is_graph=False)))
    else:
        if cc.text is None:
            raise Exception('Текст запроса пустой, нет котировки валюты')
        currency_tickers = match_many_tickers(cc.text)
        info = currency_info(currency_tickers)
        if len(info) > 0:
            result = [f'Курсы от {info["trade_day"]} {info["request_time"]} '
                      f'(изменение к закрытию {info["trade_date_before"]})', '']
            for i in currency_tickers:
                result.append(info[i]['full_info'])
            markup = markup_transitions(
                [back_transition, currency_graph_transition(currency_tickers)], drop_this=False
            )
            cc.bot.send_message(cc.chat_id, '\n'.join(result), reply_markup=markup)
        else:
            cc.bot.send_message(cc.chat_id, f"Не удалось определить валюту. "
                                            f"Мне знакомы: {','.join(AVAILABLE_CURRENCY.keys())}")
        cc.database.set_route(cc.message_author)


def currency_graph(cc: CallContext):
    if cc.trigger_by_command and cc.triggered_without_param:
        cc.database.set_route(user_id=cc.message_author, route=cc.base_route)
        cc.bot.send_message(cc.chat_id, text="Выбери нужную валюту",
                            reply_markup=markup_transitions(currency_options(is_graph=True)))
    else:
        if cc.text is None:
            raise Exception('Текст запроса пустой, нет котировки валюты')
        currency_tickers = match_many_tickers(cc.text)
        for i in currency_tickers:
            try:
                curr = currency_data(i)
                cc.bot.send_photo(cc.chat_id, photo=add_fleppa_wm(currency_plot(curr[0], curr[1], i), 100, 50),
                                  caption=f'Вот тебе график {i}/RUB')
            except Exception as e:
                cc.logger.e(f'Got exception while drawing {i}: ' + str(e))
                cc.bot.send_message(cc.chat_id, f"Не удалось построить график для {i}")
        cc.bot.send_message(cc.chat_id, 'Если ты знаешь, как сделать этот график лучше — оставь свой отзыв, '
                                        'вызвав команду /feedback',
                            reply_markup=markup_transitions([back_transition], drop_this=False))
        cc.database.set_route(cc.message_author)
