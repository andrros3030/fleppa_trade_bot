import datetime


class OneDayData:
    def __init__(self, ticker: str, change: float, volume: int):
        _ticker = ticker
        _change = change
        _volume = volume


def _get_date_data(date: datetime.date, ticker: list) -> dict:
    dct = {}
    for el in ticker:
        # TODO: add an A
        dct[el] = OneDayData(
            ticker=el,
            change=100,
            volume=100
                             )
    return dct


class TodayData:
    _date: datetime.date
    _historical: list

    def __init__(self, date: datetime.date = datetime.datetime.now().today()):
        _date = date
        _historical = []  # _get_date_data(date, ticker=['MOEX'])
