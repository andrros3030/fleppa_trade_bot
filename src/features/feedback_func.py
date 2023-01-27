"""
DO NOT IMPORT BASE_MODULES, OTHER FEATURES OR ROOT MODULES EXCEPT CONTEXT
"""
from src.context import CallContext, global_context


def feedback_start(cc: CallContext):
    if cc.database.is_banned(cc.message_author):
        cc.bot.send_message(cc.chat_id, 'Отправка фидбэка недоступна')
        return
    cc.database.set_route(cc.message_author, route=cc.base_route)
    cc.bot.send_message(cc.chat_id, 'Пожалуйста, отправьте свой фид-бэк о работе бота. '
                                    'Вы можете добавить фото или видео, админы посмотрят их и вернутся в чат')


def feedback_finish(cc: CallContext):
    for feedback_chat in global_context.FEEDBACK_CHAT_ID:
        res = cc.bot.forward_message(feedback_chat, cc.chat_id, cc.message_id)
        cc.database.save_feedback_origin(
            user_id=cc.message_author,
            origin_message_id=cc.message_id,
            forwarded_message_id=res.message_id
        )
    cc.bot.send_message(cc.chat_id, reply_to_message_id=cc.message_id, text='Фид-бэк отправлен админам, спасибо')
    cc.database.set_route(cc.message_author)
