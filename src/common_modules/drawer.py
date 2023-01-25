"""
NO PROJECT IMPORTS EXCEPT BASE_MODULES
"""
import io
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import datetime as dt
import requests


def currency_data(currency):
    today = dt.date.today()
    today_month_ago = today - dt.timedelta(days=60)
    params = {'from': today_month_ago, 'till': today}
    url = 'http://iss.moex.com' + f'/iss/statistics/engines/futures/markets/indicativerates/securities/' \
                                  f'{currency}//rub.json'
    r = requests.get(url, params=params).json()['securities']['data']
    date_value = [dt.datetime.strptime(i[0], '%Y-%m-%d') for i in r]
    currency_value = [float(i[3]) for i in r]
    return date_value, currency_value


def currency_plot(date_value, currency_value, currency, night_theme=False):
    font_color = 'black'
    bg_color = 'white'
    if night_theme:
        font_color = '#e4e4eb'
        bg_color = '#35353d'
    photo = io.BytesIO()
    fig = plt.figure()
    axes = fig.add_axes([0, 0, 1.2, 1])  # Увечил ось x с 1 до 1.2 для более качественного отображения аннотации
    x_major_locator = plt.MultipleLocator(6)
    ax = fig.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.set_facecolor(bg_color)
    date_value = dts.date2num(date_value)
    hfmt = dts.DateFormatter('%d.%m')
    ax.xaxis.set_major_formatter(hfmt)
    axes.plot(date_value, currency_value, label=f'{currency}/RUB', color=font_color, lw=2)
    fig.patch.set_facecolor(bg_color)
    axes.set_xlabel('Дата', color=font_color)
    axes.set_ylabel(f'{currency}/RUB', color=font_color)
    axes.set_xlim(date_value[0])
    axes.tick_params(colors=font_color)
    axes.grid(axis='both', linestyle='--')
    ax.plot(date_value[-1], currency_value[-1], marker='o', color=font_color, lw=0.3)
    axes.annotate(f'{round(currency_value[-1], 1)}', xy=(date_value[-1], currency_value[-1]),
                  xytext=(date_value[-1]+0.5, currency_value[-1]-1), color=font_color)
    axes.plot(date_value, [currency_value[-1]] * len(date_value), linestyle='--', color=font_color, lw=1)
    fig.savefig(photo, format='jpg', bbox_inches='tight', dpi=300)
    photo.seek(0)
    return photo
