from datetime import datetime, timedelta
import requests


def currency_info(currency_ticker):
    today = datetime.now()
    last_trade_day = today - timedelta(days=1)

    result = {}
    for currency in currency_ticker:
        response_currency = requests.get(
            f'https://iss.moex.com/iss/engines/currency/markets/index/securities/{currency}'
            f'FIX/trades.json?reversed=1&limit=1')
        currency_data_today = response_currency.json()['trades']['data'][0][-1]

        currency_value = []
        while len(currency_value) == 0:
            response_currency = requests.get(
                f"https://iss.moex.com/iss/history/engines/currency/markets/index/securities.json?date="
                f"{last_trade_day.strftime('%Y-%m-%d')}")
            currency_columns = response_currency.json()['history']['columns']
            currency_value = response_currency.json()['history']['data']

            last_trade_day -= timedelta(days=1)

        for i in currency_value:
            if f'{currency}FIX' in i:
                currency_data_last = dict(zip(currency_columns, i))['CLOSE']

        currency_change = round((currency_data_today - currency_data_last) / currency_data_today * 100, 2)

        if currency_change < 0:
            currency_content = f'{currency}: {currency_data_today} ({currency_change} % 🔴)'
        elif currency_change > 0:
            currency_content = f'{currency}: {currency_data_today} ({currency_change} % 🟢)'
        else:
            currency_content = f'{currency}: {currency_data_today} ({currency_change} % ⚪)'

        result.update({f"{currency.upper()}": {'value': currency_data_today, 'change': f'{currency_change}',
                                               'full_info': f'{currency_content}'}})

        last_trade_day = today - timedelta(days=1)

    return result
