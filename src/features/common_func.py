from src.base_modules.constants import MENU_MESSAGE
from src.common_modules.markups import menu_transitions, markup_transitions, back_transition
from src.call_context import CallContext


def menu(cc: CallContext):
    if cc.current_route != cc.base_route:
        # Если пользователь не находится в корневой позиции - возвращаем его в корень.
        # Это нужно, если пользователь выходит из команд с помощью кнопок "назад"
        cc.unfocus()
    return cc.bot.send_message(cc.chat_id, MENU_MESSAGE,
                               reply_markup=markup_transitions(menu_transitions)
                               )


def say_welcome(cc: CallContext):
    start_link = None
    if cc.text is not None and len(cc.text.split()) > 1:
        start_link = cc.text.split()[1]
    cc.database.save_user(user_id=cc.message_author, involve_link=start_link)
    cc.bot.send_message(cc.chat_id, cc.database.get_start_message(start_link),
                        reply_markup=markup_transitions(
                            [back_transition.copy('Перейти в меню')]
                        ))
