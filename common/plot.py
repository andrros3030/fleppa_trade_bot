import io
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
import datetime as dt
import requests


def currency_data(currency):
    today = dt.date.today()
    today_month_ago = today - dt.timedelta(days=60)
    params = {'from': today_month_ago, 'till': today}
    url = 'http://iss.moex.com' + f'/iss/statistics/engines/futures/markets/indicativerates/securities/' \
                                  f'{currency}//rub.json'
    r = requests.get(url, params=params).json()['securities']['data']
    date_value, currency_value = [i[0] for i in r], [float(i[3]) for i in r]
    # print(date_value, currency_value, sep='\n')
    return date_value, currency_value


def get_plot(date_value, currency_value, currency, night_theme=False):
    photo = io.BytesIO()
    fig = plt.figure()
    axes = fig.add_axes([0, 0, 1, 1])
    x_major_locator = MultipleLocator(10)  # Установите интервал масштабирования оси x на 2 и сохраните его в переменной
    ax = fig.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    if night_theme:
        ax.set_facecolor('#35353d')
        axes.plot(date_value, currency_value, label=f'{currency}/RUB', color='#e4e4eb', lw=2)
        fig.patch.set_facecolor('#35353d')
        axes.set_xlabel('DATE', color='#e4e4eb')
        axes.set_ylabel(f'{currency}/RUB', color='#e4e4eb')
        axes.tick_params(colors='#e4e4eb')  # Задаем цвет значений по верт/гориз.
    else:
        ax.set_facecolor('white')
        axes.plot(date_value, currency_value, label=f'{currency}/RUB', color='black', lw=2)
        axes.set_xlabel('DATE', color='black')
        axes.set_ylabel(f'{currency}/RUB', color='black')
        axes.tick_params(colors='black')
    axes.grid(axis='both', linestyle='--')
    fig.savefig(photo, format='jpg', bbox_inches='tight')
    photo.seek(0)
    return plt.show()


get_plot(*currency_data('USD'), 'USD', True)


# get_plot(*currency_data('EUR'), 'EUR')
def trade_line():
    x = np.arange(0, 10)
    y = 2**x
    plt.scatter(x, y)
    z = np.polyfit(x, y, 2)
    p = np.poly1d(z)
    plt.plot(x, p(x))
    plt.show()


def nigth_theme(nigth_theme):
    fig = plt.figure()
    axes = fig.add_axes([0, 0, 1, 1])
    axes.plot()

def proba():
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(-3 * np.pi, 3 * np.pi, 200)
    y = np.sinc(x)

    fig = plt.figure()

    ax_1 = fig.add_subplot(2, 1, 1)
    ax_2 = fig.add_subplot(2, 2, 3)
    ax_3 = fig.add_subplot(2, 2, 4)

    ax_1.plot(x, y)
    ax_1.grid(axis='x')
    ax_1.set_title('axis = "x"')

    ax_2.plot(x, y)
    ax_2.grid(axis='y')
    ax_2.set_title('axis = "y"')

    ax_3.plot(x, y)
    ax_3.grid(axis='both')
    ax_3.set_title('axis = "both"')

    fig.set_figwidth(12)
    fig.set_figheight(12)

    plt.show()

# proba()