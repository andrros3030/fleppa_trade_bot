"""
Кажется что этот файл станет навигатором в будущем, вынести работу с роутами сюда?
NO PROJECT IMPORTS EXCEPT BASE_MODULES
"""
from typing import List

from src.base_modules.constants import AVAILABLE_CURRENCY
from src.base_modules.routes import MENU_ROUTE, DROP_PREV_ARG, ParsedRoute, DATA_ARG, \
    CURRENCY_ROUTE, TOTEM_ROUTE, FEEDBACK_ROUTE, DIPLOMA_ROUTE, CURRENCY_GRAPH_ROUTE
from telebot.util import quick_markup
from telebot.types import InlineKeyboardMarkup


class MarkupRoute(ParsedRoute):
    def __init__(self, route: ParsedRoute, text: str):
        super().__init__(str(route))  # TODO: костыль с неоптимальной перегонкой туда-сюда всех параметров
        self.text = text

    def with_drop(self, drop=True):
        self.set_arg(
            key=DROP_PREV_ARG,
            value=drop
        )
        return self

    def copy(self, new_text):
        return MarkupRoute(route=self.route, text=new_text)


def markup_transitions(routes: List[MarkupRoute], drop_this=True) -> InlineKeyboardMarkup:
    return quick_markup({el.text: {'callback_data': str(el.with_drop(drop_this))} for el in routes})


def currency_options(is_graph: bool, currencies: List[str] or None = None) -> List[MarkupRoute]:
    if currencies is None:
        currencies = list(AVAILABLE_CURRENCY.keys())
    result = [MarkupRoute(
        text=el,
        route=ParsedRoute(ParsedRoute.serialize(CURRENCY_GRAPH_ROUTE if is_graph else CURRENCY_ROUTE,
                                                {DATA_ARG: el}))  # TODO: кажется костыль
    ) for el in currencies]
    result.append(MarkupRoute(
        text="Отобразить все",
        route=ParsedRoute(ParsedRoute.serialize(CURRENCY_GRAPH_ROUTE if is_graph else CURRENCY_ROUTE,
                                                {DATA_ARG: currencies}))  # TODO: кажется костыль
    ))
    result.append(back_transition)
    return result


def currency_graph_transition(currencies: List[str] or None) -> MarkupRoute:
    return MarkupRoute(
        text="Пострить график",
        route=ParsedRoute(ParsedRoute.serialize(CURRENCY_GRAPH_ROUTE,
                                                {DATA_ARG: currencies}))  # TODO: кажется костыль
    )


def back_transition_markup(drop_this=True) -> InlineKeyboardMarkup:
    return markup_transitions([back_transition], drop_this=drop_this)


back_transition = MarkupRoute(ParsedRoute(MENU_ROUTE), text='Назад к меню')
diploma_transition = MarkupRoute(ParsedRoute(DIPLOMA_ROUTE), text='Получить диплом')
menu_transitions = [
    MarkupRoute(ParsedRoute(CURRENCY_ROUTE), text='Курсы валют'),
    MarkupRoute(ParsedRoute(TOTEM_ROUTE), text='Кто я на бирже'),
    MarkupRoute(ParsedRoute(FEEDBACK_ROUTE), text='Оставить отзыв'),
]
# TODO: сократить markup_transitions([back_transition]) до only_back
