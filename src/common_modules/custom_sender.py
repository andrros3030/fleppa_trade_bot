from telebot.apihelper import ApiTelegramException


def try_to_send(bot, chat_id, message_text, logger):
    """
    Функцию нужно использовать всегда, когда пользователь мог забанить бота.
    Например, если бот отвечает на команду не сразу или если это общая рассылка

    :param bot: экземпляр бота

    :param chat_id: id чата, в который отправляется сообщение

    :param message_text: текст для отправки

    :param logger:
    :return: True если удалось отправить сообщение, иначе False
    """
    try:
        bot.send_message(chat_id, message_text)
        return True
    except ApiTelegramException as e:
        if e.description == "Forbidden: bot was blocked by the user" or str(e.error_code) == "403":
            logger.w(f"User {chat_id} blocked bot")
        return False


def send_long_message(bot, chat_id, message_text, logger):
    if len(message_text) > 4095:
        for x in range(0, len(message_text), 4095):
            try_to_send(bot, chat_id, message_text[x:x + 4095], logger)
    else:
        try_to_send(bot, chat_id, message_text, logger)
