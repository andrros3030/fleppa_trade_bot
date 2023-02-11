"""
DO NOT IMPORT BASE_MODULES, OTHER FEATURES OR ROOT MODULES EXCEPT CONTEXT
"""
from src.common_modules.custom_sender import send_long_message
from src.call_context import CallContext
import requests


# TODO: deprecate calling functions with args
# TODO: change cc.database.set_route to cc. focus / unfocus


def set_admin(cc: CallContext):
    if cc.text.lower() == 'exit':
        cc.unfocus()
        return cc.bot.send_message(cc.chat_id, 'Выполнение команды прекращено')
    if cc.base_trigger:
        cc.focus()
        return cc.bot.send_message(cc.chat_id, 'Введи id человека, которого хочешь сделать админом')
    else:
        cc.unfocus()
        return cc.bot.send_message(cc.chat_id,
                                   str(cc.database.set_admin(cc.text)))


def exec_sql(cc: CallContext):
    if cc.text.lower() == 'exit':
        cc.unfocus()
        return cc.bot.send_message(cc.chat_id, 'Выполнение команды прекращено')
    if cc.base_trigger:
        cc.focus()
        return cc.bot.send_message(cc.chat_id, 'Перешел в режим выполнения SQL. Набери exit, чтобы выйти')
    else:
        query_result = cc.database.unsafe_exec(cc.text)
        cc.bot.send_message(cc.chat_id, f'Выполняют SQL запрос: {cc.text}; Набери exit чтобы прекратить')
        if type(query_result) is list or type(query_result) is tuple:
            query_result = '\n'.join(map(str, query_result))
        else:
            query_result = str(query_result)
        return send_long_message(bot=cc.bot, chat_id=cc.chat_id, logger=cc.logger,
                                 message_text=query_result)


def get_environment(cc: CallContext):
    return cc.bot.send_message(cc.chat_id, str(cc.env_context))


def make_link(cc: CallContext):
    if cc.text.lower() == 'exit':
        cc.unfocus()
        return cc.bot.send_message(cc.chat_id, 'Выполнение команды прекращено')
    if cc.base_trigger:
        cc.focus()
        cc.bot.send_message(cc.chat_id, 'Введи описание для новой ссылки')
    else:
        if cc.current_route.get_arg("description") is None:
            cc.current_route.set_arg("description", cc.text)
            cc.focus(cc.current_route)
            cc.bot.send_message(cc.chat_id, 'Введите новое приветственное сообщение или skip')
        else:
            start_message = None
            description = cc.current_route.get_arg("description")[0]
            if cc.text.lower() not in ['skip', 'скип']:
                start_message = cc.text
            link = cc.database.generate_link(description=description, startup_message=start_message)
            cc.unfocus()
            if link is None:
                return cc.bot.send_message(cc.chat_id, 'Не удалось создать ссылку. Проверь логи взаимодействия с БД.')
            return cc.bot.send_message(cc.chat_id, 't.me/' + cc.bot.get_me().username + '?start=' + link)


def simulate_crash(cc: CallContext):
    cc.bot.send_message(cc.chat_id, 'Крашаюсь, проверяй')
    raise Exception('Краш вызван специально')


def make_request(cc: CallContext):
    if cc.text.lower() == 'exit':
        cc.unfocus()
        return cc.bot.send_message(cc.chat_id, 'Выполнение команды прекращено')
    if cc.base_trigger:
        cc.focus()
        return cc.bot.send_message(cc.chat_id, 'Введите тип запроса (get)')
    else:
        if cc.current_route.get_arg('method') is None:
            cc.current_route.set_arg('method', cc.text)
            return cc.bot.send_message(cc.chat_id, 'Введите url-адрес')
        else:
            cc.unfocus()
            res = requests.request(cc.current_route.get_arg('method')[0], cc.text)
            return send_long_message(bot=cc.bot, chat_id=cc.chat_id, logger=cc.logger,
                                     message_text=str(res.status_code) + ': ' + str(res.headers) + '\n' + str(
                                         res.reason))


def stats(cc: CallContext):
    dct = {
           't_users': 'ts_reg',
           't_messages': 'ts_saved',
           't_feedback': 'ts_requested'
          }
    res = []
    for key in dct:
        query = (f'select count(*) as total, '
                 f'sum(case when current_date - cast({dct[key]} as date) <= 1 then 1 else 0 end) as Daily, '
                 f'sum(case when current_date - cast({dct[key]} as date) <= 7 then 1 else 0 end) as Weekly, '
                 f'sum(case when current_date - cast({dct[key]} as date) <= 30 then 1 else 0 end) as Monthly '
                 f'from {key};')
        query_result = cc.database.unsafe_exec(query)[0]
        res.append(f'{key} {query_result[0]}(+{query_result[1]} за день, +{query_result[2]} за неделю, '
                   f'+ {query_result[3]} за месяц).')
    return cc.bot.send_message(cc.chat_id, '\n'.join(res))
