from src.common_modules.request_currency import currency_info


count = 0
for _ in range(10000):
    info = currency_info('USD')
    trade_day = info["trade_day"]
    last_time = info["request_time"]
    prev_trade_day = info["trade_date_before"]
    count += 1
    print(count)
    # print(info['full_info'])
    # print(info)
