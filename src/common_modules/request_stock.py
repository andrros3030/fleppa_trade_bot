import requests


def stock_price(ask):
    try:
        response_stocks = requests.get(
            'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json')
        while True:
            try:
                market_data = response_stocks.json()['marketdata']['data']
                counter = 0
                while True:
                    if ask.upper() in market_data[counter]:
                        return f'цена {ask.upper()} - {market_data[counter][12]}'
                    else:
                        counter += 1
            except IndexError:
                securities_data = response_stocks.json()['securities']['data']
                new_securities_data = []
                for i in securities_data:
                    i = list(map(str, i))
                    i = [j.upper() for j in i]
                    new_securities_data.append(i)
                ticker = []
                if ' ' in ask:
                    temporary_ask = ask.split()[0]
                else:
                    temporary_ask = ask
                for i in new_securities_data:
                    for j in i:
                        if temporary_ask.upper() in j:
                            if i in ticker:
                                continue
                            else:
                                ticker.append(i)
                        else:
                            continue

                if len(ticker) > 1:
                    if ('П' or 'ПР') in ask.split()[-1][0:2].upper():
                        symbols_p = ask.upper().count('П')
                        if ticker[0][2].count('П') + symbols_p != ticker[0][2].count('П'):
                            for i in ticker:
                                if i[9].split()[-1] == 'АП':
                                    ticker = ticker[ticker.index(i)]
                                    break
                                else:
                                    continue
                    else:
                        for i in ticker:
                            if ask.upper() in (i[9] or i[2]):
                                ticker = ticker[ticker.index(i)]
                                break
                ask = ticker[0]
    except IndexError:
        raise 'Неправильно введен запрос, попробуйте изменить его'
