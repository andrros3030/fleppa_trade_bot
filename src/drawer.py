import io
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import datetime as dt
import requests


def currency_data(currency):
    today = dt.date.today()
    today_month_ago = today - dt.timedelta(days = 14)
    parametrs = {'from': today_month_ago,  'till': today}
    url = 'http://iss.moex.com' + f'/iss/statistics/engines/futures/markets/indicativerates/securities/{currency}//rub.json'
    r = requests.get(url, params=parametrs).json()['securities']['data']
    date_value, currency_value = [i[0] for i in r], [int(i[3]) for i in r]
    return date_value, currency_value


def get_plot(date_value, currency_value, currency):
    my_stringIObytes = io.BytesIO()
    fig = plt.figure()
    axes = fig.add_axes([0, 0, 1, 1])
    axes.set_xlabel('DATE')
    axes.set_ylabel(f'{currency}/RUB')
    x_major_locator = MultipleLocator(2)  # Установите интервал масштабирования оси x на 2 и сохраните его в переменной
    ax = fig.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    axes.plot(date_value, currency_value, label=f'{currency}/RUB', color='red')
    fig.savefig(my_stringIObytes, format='jpg', bbox_inches='tight')
    my_stringIObytes.seek(0)
    return my_stringIObytes

