"""
DO NOT IMPORT BASE_MODULES, OTHER FEATURES OR ROOT MODULES EXCEPT CONTEXT
"""
from src.common_modules.custom_sender import send_long_message
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
    return send_long_message(bot=cc.bot, chat_id=cc.chat_id, logger=cc.logger,
                             message_text=query_result)


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
    return send_long_message(bot=cc.bot, chat_id=cc.chat_id, logger=cc.logger,
                             message_text=str(res.status_code) + ': ' + str(res.headers) + '\n' + str(res.reason))


def stats(cc: CallContext):
    users_query = 'select count(*) as total, ' \
                  'sum(case when current_date - cast(ts_reg as date) <= 1 then 1 else 0 end) as Daily, ' \
                  'sum(case when current_date - cast(ts_reg as date) <= 7 then 1 else 0 end) as Weekly, ' \
                  'sum(case when current_date - cast(ts_reg as date) <= 30 then 1 else 0 end) as Monthly ' \
                  'from t_users;'
    messages_query = 'select count(*) as total, ' \
                     'sum(case when current_date - cast(ts_saved as date) <= 1 then 1 else 0 end) as Daily, ' \
                     'sum(case when current_date - cast(ts_saved as date) <= 7 then 1 else 0 end) as Weekly, ' \
                     'sum(case when current_date - cast(ts_saved as date) <= 30 then 1 else 0 end) as Monthly ' \
                     'from t_messages;'
    fb_query = 'select count(*) as total, ' \
               'sum(case when current_date - cast(ts_requested as date) <= 1 then 1 else 0 end) as Daily, ' \
               'sum(case when current_date - cast(ts_requested as date) <= 7 then 1 else 0 end) as Weekly, ' \
               'sum(case when current_date - cast(ts_requested as date) <= 30 then 1 else 0 end) as Monthly ' \
               'from t_feedback;'
    users_query = cc.database.unsafe_exec(users_query)
    messages_query = cc.database.unsafe_exec(messages_query)
    fb_query = cc.database.unsafe_exec(fb_query)
    return cc.bot.send_message(cc.chat_id, f'Пользователей: {users_query[0][0]} '
                                           f'(+{users_query[0][1]} за день/ '
                                           f'+{users_query[0][2]} за неделю/'
                                           f'+{users_query[0][3]} за месяц).\n'
                                           f'Сообщений: {messages_query[0][0]} '
                                           f'(+{messages_query[0][1]} за день/ '
                                           f'+{messages_query[0][2]} за неделю/ '
                                           f'+{messages_query[0][3]} за месяц).\n'
                                           f'Фидбэка: {fb_query[0][0]} '
                                           f'(+{fb_query[0][1]} за день/ '
                                           f'+{fb_query[0][2]} за неделю/ '
                                           f'+{fb_query[0][3]} за месяц).')
