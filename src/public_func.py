from src.constants import global_context, CallContext
from src.request_currency import currency_info
from src.drawer import currency_plot, currency_data
from src.homiak_diploma import diploma


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
            return cc.bot.send_message(cc.chat_id, 'Команда доступна при ответе на сообщение')
        if cc.reply_data.forward_from is None:
            return cc.bot.send_message(cc.chat_id, 'Сообщение не похоже на фидбэк, фидбэк должен быть переслан')
        feedback_author = cc.reply_data.forward_from
        if cc.reply_data.from_user.id != cc.bot.get_me().id:
            return cc.bot.send_message(cc.chat_id, f'Команда доступна только для моих '
                                                   f'(@{cc.bot.get_me().username}) сообщений')

        route_params = f'?chat_id={feedback_author.id}&&message_id={cc.reply_data.message_id}'
        cc.database.set_route(cc.message_author, route=cc.base_route + route_params)
        cc.bot.send_message(cc.chat_id, f"Напиши ответ на фид-бэк от пользователя: "
                                        f"@{str(feedback_author.username)}, id='{feedback_author.id}', "
                                        f"message_id={cc.reply_data.message_id}")
    else:
        reply_chat_id = cc.current_route.args['chat_id']
        reply_forwarded = cc.current_route.args['message_id']
        if reply_chat_id is None or reply_forwarded is None:
            return cc.bot.send_message(cc.chat_id, f'Не удалось ответить на сообщение с пустым chat_id или message_id: '
                                                   f'{str(cc.current_route)}')
        reply_id = cc.database.get_feedback_origin(
            forwarded_message_id=reply_forwarded,
            author_id=reply_chat_id
        )
        if reply_id is None:
            return cc.bot.send_message(cc.chat_id, 'Не удалось найти initial message id в базе данных')
        if cc.content_type == 'text':
            cc.bot.send_message(reply_chat_id, reply_to_message_id=reply_id, text=cc.text)
        elif cc.content_type == 'photo':
            # TODO: костыль, нужно итерироваться по фоткам
            cc.bot.send_photo(reply_chat_id, reply_to_message_id=reply_id, photo=cc.photo[0].file_id,
                              caption=cc.caption)
        elif cc.content_type == 'sticker':
            cc.bot.send_sticker(reply_chat_id, reply_to_message_id=reply_id, sticker=cc.sticker.file_id)
        else:
            return cc.bot.send_message(cc.chat_id, f'Не могу переслать контент типа {cc.content_type}, '
                                                   f'пока способен пересылать только текст, изображения или стикеры. '
                                                   f'Пожалуйста, напиши новый ответ')
        res = cc.bot.send_message(cc.chat_id, 'Ответ отправлен').message_id
        cc.database.resolve_feedback(cc.message_author, reply_id, reply_forwarded)
        resolve_time = cc.database.get_resolve_time(cc.message_author, reply_forwarded)
        if resolve_time is None:
            resolve_time = -60
        cc.bot.edit_message_text(chat_id=cc.chat_id, message_id=res,
                                 text=f'Отвечено за {resolve_time//60} минут')
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


def get_diploma(cc: CallContext):
    lastname = cc.user_data.last_name
    if lastname is None:
        lastname = ""
    else:
        lastname = " " + lastname
    cc.bot.send_photo(cc.chat_id, photo=diploma(cc.user_data.first_name + lastname))


def currency_graph(cc: CallContext):
    currency_tickers = ['USD', 'EUR']
    for i in currency_tickers:
        curr = currency_data(i)
        cc.bot.send_photo(cc.chat_id, photo=currency_plot(curr[0], curr[1], i), caption=f'Вот тебе график {i}/RUB')