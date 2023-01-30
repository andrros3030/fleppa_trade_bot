"""
NO PROJECT IMPORTS EXCEPT BASE_MODULES
"""
from datetime import datetime, timedelta
import requests


def currency_info(currency: str):
    url_today = f'http://iss.moex.com/iss/engines/currency/markets/index/securities/{currency}' \
                f'FIX/trades.json'
    try:
        response_currency = requests.get(url_today, params={'reversed': True, 'limit': 1})
        currency_data_today = response_currency.json()['trades']['data'][0][-1]
        today = response_currency.json()['trades']['data'][0][-4]
        time = response_currency.json()['trades']['data'][0][-2]

    except Exception as e:
        raise Exception(f"Can't get data with this URL: {url_today}. Causing error: {str(e)}")

    currency_value = []
    last_trade_day = datetime.strptime(today, '%Y-%m-%d') - timedelta(days=1)
    url_last_trade_date = "http://iss.moex.com/iss/history/engines/currency/markets/index/securities.json"
    while len(currency_value) == 0:
        try:
            response_currency = requests.get(url_last_trade_date, params={"date": last_trade_day})
            currency_columns = response_currency.json()['history']['columns']
            currency_value = response_currency.json()['history']['data']
        except Exception as e:
            raise Exception(f"Can't get data with this URL: {url_last_trade_date}. Causing error: {str(e)}")

        if len(currency_value) == 0:
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
    return {'value': currency_data_today, 'change': f'{currency_change}',
            'full_info': f'{currency_content}',
            'trade_day': f'{datetime.strptime(today, "%Y-%m-%d").strftime("%d-%m")}',
            'trade_date_before': f'{last_trade_day.strftime("%d-%m")}', 'request_time': f'{time}'}
