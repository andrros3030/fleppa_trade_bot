"""
Динамическая генерация сообщения-подсказки для корневой команды.
Корневая команда в данном случае может быть реальным корнем ("/") или внутренней командой ("/feedback")
"""
from src.context import CallContext


def generate_help(cc: CallContext):
    """
    Автоматически генерирует сообщение помощи для отображения всех команд родительской (корневой) команды

    :param cc: контекст вызова функции
    """
    all_commands = []
    for cmd in cc.root_command.inner_commands:
        if (cc.is_admin or cmd.public) and cmd.show_in_help:
            all_commands.append(str(cmd))
    res = '\n'.join(all_commands)
    return cc.bot.send_message(cc.chat_id, res)


def help_with_unmatched(cc: CallContext):
    """
    Команда для вывода, если не удалось смэтчить никакую другую команду

    :param cc: контекст вызова функции
    """
    return cc.bot.send_message(cc.chat_id, 'Кажется я не знаю такой команды. Попробуй /help')


def go_back(cc: CallContext):
    """
    Команда для возврата в корневую позицию ('/')
    Выводит inner_fields['text'] пользователю
    """
    cc.database.set_route(cc.message_author)
    msg = 'Вышел из команды'
    print(cc.root_command)
    if cc.root_command.inner_fields is not None and 'go_back_text' in cc.root_command.inner_fields:
        msg = cc.root_command.inner_fields['go_back_text']
    cc.bot.send_message(cc.chat_id, text=msg)
