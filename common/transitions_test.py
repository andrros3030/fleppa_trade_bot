from src.base_modules.routes import ParsedRoute, DROP_PREV_ARG, DATA_ARG
from src.common_modules.markups import markup_transitions, MarkupRoute, currency_options


def test_base():
    test1 = ParsedRoute('/test1')
    test2 = ParsedRoute('/test2?currency=USD')
    trans1, trans2 = markup_transitions(
        [MarkupRoute(test1, 'without param'), MarkupRoute(test2, 'with param')]
    ).keyboard[0]
    print(trans1)
    print(trans2)
    parsing1 = ParsedRoute(trans1.callback_data)
    parsing2 = ParsedRoute(trans2.callback_data)
    print(parsing1.route, parsing1)
    print(parsing2.route, parsing2)
    assert parsing2.get_arg('currency') == 'USD'
    assert parsing2.get_arg(DROP_PREV_ARG)
    print('everything ok')


def test_currencies():
    trans1 = markup_transitions(currency_options()).keyboard[0][0]
    print(trans1)
    parsing1 = ParsedRoute(trans1.callback_data)
    print(parsing1.route, parsing1)
    print(parsing1.get_arg(DATA_ARG))


test_currencies()
test_base()
