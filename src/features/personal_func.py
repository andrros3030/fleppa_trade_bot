from src.call_context import CallContext
from src.common_modules.homiak_diploma import diploma
from src.common_modules.markups import back_transition, markup_transitions, diploma_transition
from src.common_modules.photoshop import add_fleppa_wm


def get_totem(cc: CallContext):
    cc.bot.send_message(cc.chat_id, str(cc.totem), reply_markup=markup_transitions(
        [back_transition, diploma_transition], drop_this=False
    ))


def get_diploma(cc: CallContext):
    lastname = cc.user_data.last_name
    if lastname is None:
        lastname = ""
    else:
        lastname = " " + lastname
    cc.bot.send_photo(cc.chat_id, photo=add_fleppa_wm(diploma(cc.user_data.first_name + lastname, cc.totem.totem),
                                                      x=397, y=1584),
                      caption='Похвастайся друзьям дипломом и узнай, кто они на бирже 😱',
                      reply_markup=markup_transitions([back_transition], drop_this=False))
