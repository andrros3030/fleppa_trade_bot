"""
DO NOT IMPORT BASE_MODULES, OTHER FEATURES OR ROOT MODULES EXCEPT CONTEXT
"""
from src.context import global_context, CallContext
import requests


def set_admin(cc: CallContext):
    if len(cc.splitted_message) != 2:
        return cc.bot.send_message(cc.chat_id, 'Комманда принимает на вход один аргумент - id человека, '
                                               'назначаемого админом')
    return cc.bot.send_message(cc.chat_id, str(cc.database.set_admin(cc.splitted_message[1])))


def exec_sql(cc: CallContext):
    query_result = cc.database.unsafe_exec(' '.join(cc.splitted_message[1:]))
    if type(query_result) is list or type(query_result) is tuple:
        query_result = '\n'.join(map(str, query_result))
    else:
        query_result = str(query_result)
    return cc.bot.send_message(cc.chat_id, query_result)


def get_environment(cc: CallContext):
    return cc.bot.send_message(cc.chat_id, str(global_context))


def make_link(cc: CallContext):
    if len(cc.splitted_message) < 2:
        cc.bot.send_message(cc.chat_id, 'Введите описание создаваемой ссылки и, '
                                        'если необходимо, стартовое сообщение через ;')
        return
    content = ' '.join(cc.splitted_message[1:])
    desc = content.split(';')[0]
    sm = content.split(';')[1] if len(content.split(';')) > 1 else None
    link = cc.database.generate_link(description=desc, startup_message=sm)
    if link is None:
        return cc.bot.send_message(cc.chat_id, 'Не удалось создать ссылку. Проверь логи взаимодействия с БД.')
    return cc.bot.send_message(cc.chat_id, 't.me/' + cc.bot.get_me().username + '?start=' + link)


def simulate_crash(cc: CallContext):
    cc.bot.send_message(cc.chat_id, 'Крашаюсь, проверяй')
    raise Exception('Краш вызван специально')


def make_request(cc: CallContext):
    if len(cc.splitted_message) != 3:
        return cc.bot.send_message(cc.chat_id, 'Команда принимает на вход тип запроса и адрес ресурса через пробел')
    _, method, resource_link = map(str, cc.splitted_message)
    res = requests.request(method, resource_link)
    cc.bot.send_message(cc.chat_id, str(res.status_code) + ': ' + str(res.headers) + '\n' + str(res.reason))


def stats(cc: CallContext):
    query_total_users = 'select count(*) from t_users'
    query_daily_users = 'select count(*) from t_users where current_date - cast(ts_reg as date) <= 1;'
    query_weekly_users = 'select count(*) from t_users where current_date - cast(ts_reg as date) <= 7;'
    query_monthly_users = 'select count(*) from t_users where current_date - cast(ts_reg as date) <= 30;'
    query_total_messages = 'select count(*) from t_messages'
    query_daily_messages = 'select count(*) from t_messages where current_date - cast(ts_saved as date) <= 1;'
    query_weekly_messages = 'select count(*) from t_messages where current_date - cast(ts_saved as date) <= 7;'
    query_monthly_messages = 'select count(*) from t_messages where current_date - cast(ts_saved as date) <= 30;'
    query_total_fb = 'select count(*) from t_feedback'
    query_daily_fb = 'select count(*) from t_feedback where current_date - cast(ts_requested as date) <= 1;'
    query_weekly_fb = 'select count(*) from t_feedback where current_date - cast(ts_requested as date) <= 7;'
    query_monthly_fb = 'select count(*) from t_feedback where current_date - cast(ts_requested as date) <= 30;'
    users_info = f'Пользователей: {cc.database.unsafe_exec(query_total_users)[0][0]} ' \
                 f'(+{cc.database.unsafe_exec(query_daily_users)[0][0]} за день/ ' \
                 f'+{cc.database.unsafe_exec(query_weekly_users)[0][0]} за неделю/ ' \
                 f'+{cc.database.unsafe_exec(query_monthly_users)[0][0]} за месяц).\n'
    messages_info = f'Сообщений: {cc.database.unsafe_exec(query_total_messages)[0][0]} ' \
                    f'(+{cc.database.unsafe_exec(query_daily_messages)[0][0]} за день/ ' \
                    f'+{cc.database.unsafe_exec(query_weekly_messages)[0][0]} за неделю/ ' \
                    f'+{cc.database.unsafe_exec(query_monthly_messages)[0][0]} за месяц).\n'
    fb_info = f'Количество фидбэка: {cc.database.unsafe_exec(query_total_fb)[0][0]} ' \
              f'(+{cc.database.unsafe_exec(query_daily_fb)[0][0]} за день/ ' \
              f'+{cc.database.unsafe_exec(query_weekly_fb)[0][0]} за неделю/ ' \
              f'+{cc.database.unsafe_exec(query_monthly_fb)[0][0]} за месяц).\n'
    return cc.bot.send_message(cc.chat_id, users_info + messages_info + fb_info)
