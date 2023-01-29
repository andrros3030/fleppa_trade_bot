from src.context import CallContext, global_context
from telebot.apihelper import ApiTelegramException
from src.common_modules.markups import back_transition, markup_transitions


def reply(cc: CallContext):
    if cc.current_route.route != cc.base_route:
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
        reply_chat_id = cc.current_route.get_arg('chat_id')
        reply_forwarded = cc.current_route.get_arg('message_id')
        if reply_chat_id is None or reply_forwarded is None:
            return cc.bot.send_message(cc.chat_id, f'Не удалось ответить на сообщение с пустым chat_id или message_id: '
                                                   f'{str(cc.current_route)}')
        reply_id = cc.database.get_feedback_origin(
            forwarded_message_id=reply_forwarded,
            author_id=reply_chat_id
        )
        if reply_id is None:
            return cc.bot.send_message(cc.chat_id, 'Не удалось найти initial message id в базе данных')
        try:
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
                                                       f'пока способен пересылать только текст, изображения или '
                                                       f'стикеры. '
                                                       f'Пожалуйста, напиши новый ответ')
            res = cc.bot.send_message(cc.chat_id, 'Ответ отправлен').message_id
            cc.database.resolve_feedback(cc.message_author, reply_id, reply_forwarded)
            resolve_time = cc.database.get_resolve_time(cc.message_author, reply_forwarded)
            if resolve_time is None:
                resolve_time = -60
            cc.bot.edit_message_text(chat_id=cc.chat_id, message_id=res,
                                     text=f'Отвечено за {resolve_time // 60} минут')
        except ApiTelegramException as e:
            if e.description == "Forbidden: bot was blocked by the user" or str(e.error_code) == "403":
                cc.logger.w(f"User {cc.chat_id} blocked bot")
            cc.bot.send_message(cc.chat_id, f'Не удалось отправить ответ: {e.description}')
        cc.database.set_route(cc.message_author)


def send_to_public(cc: CallContext):
    print(cc.base_trigger)
    print(cc.triggered_without_param)
    # TODO: send to all (or to group) function with sql and confirmation + users count
    if cc.base_trigger and cc.triggered_without_param:
        print(1)
        # TODO: ask for message to send for everyone
        cc.database.set_route(user_id=cc.message_author, route=cc.base_route)
    else:
        print(2)
        # if True:  # cc.current_route.args is None or len(cc.current_route.args) == 0:
        #     # TODO: save message and ask for query
        #     cc.bot.send_message(cc.chat_id, "Введи блок where (и далее) для команды отбора пользователей из t_users "
        #                                     "(например: where mod(pk_id, 1) = 1 limit 100 "
        #                                     "-- вернет половину пользователей или 100, смотря чего будет меньше)")
        #     pass
        # else:
        #     # TODO: count affecting users in query, save query and ask for confirmation
        #     pass


def feedback(cc: CallContext):
    if cc.current_route != cc.base_route:
        cc.logger.i(f'feedback for {cc.message_author} started')
        if cc.database.is_banned(cc.message_author):
            cc.bot.send_message(cc.chat_id, 'Отправка фидбэка недоступна')
            return
        cc.database.set_route(cc.message_author, route=cc.base_route)
        cc.bot.send_message(cc.chat_id, 'Пожалуйста, отправьте свой фид-бэк о работе бота. '
                                        'Вы можете добавить фото или видео, админы посмотрят их и вернутся в чат',
                            reply_markup=markup_transitions(
                                [back_transition]
                            ))
    else:
        for feedback_chat in global_context.FEEDBACK_CHAT_ID:
            res = cc.bot.forward_message(feedback_chat, cc.chat_id, cc.message_id)
            cc.database.save_feedback_origin(
                user_id=cc.message_author,
                origin_message_id=cc.message_id,
                forwarded_message_id=res.message_id
            )
        cc.bot.send_message(cc.chat_id, reply_to_message_id=cc.message_id, text='Фид-бэк отправлен админам, спасибо',
                            reply_markup=markup_transitions(
                                [back_transition], drop_this=False
                            ))
        cc.database.set_route(cc.message_author)
