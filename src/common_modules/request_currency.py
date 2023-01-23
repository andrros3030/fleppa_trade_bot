"""
NO PROJECT IMPORTS EXCEPT BASE_MODULES
"""
from datetime import datetime, timedelta
import requests


def currency_info(currency_ticker):
    today = datetime.now()
    yesterday = today - timedelta(days=7)
    today, yesterday = today.strftime('%Y-%m-%d'), yesterday.strftime('%Y-%m-%d')

    result = {}

    for currency in currency_ticker:
        response_currency = requests.get(
            f'http://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/'
            f'securities/{currency}//rub.json?from={yesterday}&till={today}')
        currency_data = response_currency.json()['securities']['data']
        currency_today = currency_data[-1][-1]
        currency_change = round((currency_data[-1][-1] - currency_data[-2][-1]) / currency_data[-2][-1] * 100, 2)

        if currency_change < 0:
            currency_content = f'{currency.upper()}: {currency_today} ({currency_change} % 🔴)'
        elif currency_change > 0:
            currency_content = f'{currency.upper()}: {currency_today} ({currency_change} % 🟢)'
        else:
            currency_content = f'{currency.upper()}: {currency_today} ({currency_change} % ⚪)'

        result.update(
            {f"{currency.upper()}": {'value': currency_today, 'change': currency_change, 'full_info': currency_content}}
        )

    return result
