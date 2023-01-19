from src.constants import global_context, CallContext
from src.request_currency import currency_info


# TODO: !!!!!!!!!!!!ОБРАБОТКА ОШИБОК!!!!!!!!


def feedback(cc: CallContext):
    print(cc)
    if cc.text == '/feedback':
        if cc.database.is_banned(cc.message_author):
            cc.bot.send_message(cc.chat_id, 'Отправка фидбэка недоступна')
            return
        cc.database.set_route(cc.message_author, route=cc.base_route)
        cc.bot.send_message(cc.chat_id, 'Пожалуйста, отправьте свой фид-бэк о работе бота. '
                                        'Вы можете добавить фото или видео о работе бота')
    else:
        for feedback_chat in global_context.FEEDBACK_CHAT_ID:
            res = cc.bot.forward_message(feedback_chat, cc.chat_id, cc.message_id)
            cc.database.save_feedback_origin(
                user_id=cc.message_author,
                origin_message_id=cc.message_id,
                forwarded_message_id=res.message_id
            )
        cc.bot.send_message(cc.chat_id, reply_to_message_id=cc.message_id, text='Фид-бэк отправлен админам, спасибо')
        cc.database.set_route(cc.message_author)


def reply(cc: CallContext):
    if cc.text == '/reply':
        if cc.reply_data is None:
            cc.bot.send_message(cc.chat_id, 'Команда доступна при ответе на сообщение')
            return
        if cc.reply_data.forward_from is None:
            cc.bot.send_message(cc.chat_id, 'Сообщение не похоже на фидбэк, фидбэк должен быть переслан')
            return
        feedback_author = cc.reply_data.forward_from
        if cc.reply_data.from_user.id != cc.bot.get_me().id:
            cc.bot.send_message(cc.chat_id, f'Команда доступна только для моих (@{cc.bot.get_me().username}) сообщений')
            return
        route_params = f'?chat_id={feedback_author.id}&&message_id={cc.reply_data.message_id}'
        cc.database.set_route(cc.message_author, route=cc.base_route + route_params)
        cc.bot.send_message(cc.chat_id, f"Напиши ответ на фид-бэк от пользователя: "
                                        f"@{str(feedback_author.username)}, id='{feedback_author.id}', "
                                        f"message_id={cc.reply_data.message_id}")
    else:
        reply_chat_id = cc.current_route.args['chat_id']
        reply_forwarded = cc.current_route.args['message_id']
        if reply_chat_id is None or reply_forwarded is None:
            cc.bot.send_message(cc.chat_id, f'Не удалось ответить на сообщение с пустым chat_id или message_id: '
                                            f'{str(cc.current_route)}')
            return
        reply_id = cc.database.get_feedback_origin(
            forwarded_message_id=reply_forwarded,
            author_id=reply_chat_id
        )
        if reply_id is None:
            cc.bot.send_message(cc.chat_id, 'Не удалось найти initial message id в базе данных')
            return
        if cc.content_type == 'text':
            cc.bot.send_message(reply_chat_id, reply_to_message_id=reply_id, text=cc.text)
        elif cc.content_type == 'photo':
            # TODO: костыль, нужно итерироваться по фоткам
            cc.bot.send_photo(reply_chat_id, reply_to_message_id=reply_id, photo=cc.photo[0].file_id,
                              caption=cc.caption)
        elif cc.content_type == 'sticker':
            cc.bot.send_sticker(reply_chat_id, reply_to_message_id=reply_id, sticker=cc.sticker.file_id)
        else:
            cc.bot.send_message(cc.chat_id, f'Не могу переслать контент типа {cc.content_type}, '
                                            f'пока способен пересылать только текст, изображения или стикеры. '
                                            f'Пожалуйста, напиши новый ответ')
            return
        cc.bot.send_message(cc.chat_id, 'Ответ отправлен')
        cc.database.set_route(cc.message_author)


def say_wellcome(cc: CallContext):
    start_link = cc.splitted_message[1] if len(cc.splitted_message) > 1 else None
    cc.database.save_user(user_id=str(cc.message_author), involve_link=start_link)
    cc.bot.send_message(cc.chat_id, cc.database.get_start_message(start_link=start_link))


def currency(cc: CallContext):
    currency_tickers = ['USD', 'EUR']
    info = currency_info(currency_tickers)
    result = []
    for i in currency_tickers:
        result.append(info[i]['full_info'])

    cc.bot.send_message(cc.chat_id, '\n'.join(result))
