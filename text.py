import requests
import datetime as dt
currency = 'CNY'
url_today = f'http://iss.moex.com/iss/engines/currency/markets/index/securities/{currency}' \
                f'FIX/trades.json'
response_currency = requests.get(url_today, params={'reversed': True})
date = response_currency.json()['trades']['data']
print(dt.datetime.now())