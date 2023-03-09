import requests


def stock_price(ask):
    try:
        response_stocks = requests.get(
            'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json')
        market_data = response_stocks.json()['marketdata']['data']

        def check_ask():
            counter = 0
            try:
                while ask.upper() != market_data[counter]:
                    if ask.upper() in market_data[counter]:
                        return f'цена {ask.upper()} - {market_data[counter][12]}'
                    else:
                        counter += 1
                check_ask()
            except IndexError:
                pass

        if check_ask() is not None:
            return check_ask()

        else:
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
            if len(ticker) == 1:
                ask = ticker[0][0]
            else:
                ticker_update = []
                for i in ticker:
                    if ask.upper() in (i[9] or i[2]):
                        ticker_update = ticker[ticker.index(i)]
                        break
                if len(ticker_update) == 0:
                    symbols_p = ask.upper().count('П')
                    if ticker[0][2].count('П') + symbols_p != ticker[0][2].count('П'):
                        for i in ticker:
                            if i[9].split()[-1] == 'АП':
                                ticker_update = ticker[ticker.index(i)]
                            else:
                                continue
                ask = ticker_update[0]
            return check_ask()
    except IndexError:
        return 'Неправильно введен запрос, попробуйте изменить его'
