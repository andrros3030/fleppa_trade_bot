# from telebot import types
#
#
# class Path:
#     _popable: bool
#     _prefer_not_to_pop: bool
#     _link: str
#     _name: str
#
#
#     def __init__(self, link, popable=True, prefer_not_to_pop=False):
#         self._link = link
#         self._popable = popable
#         self._prefer_not_to_pop = prefer_not_to_pop
#
#     @property
#     def can_pop(self):
#         return self._popable
#
#     @property
#     def may_pop(self):
#         return self._popable and not self._prefer_not_to_pop
#
#     @property
#     def link(self):
#         return self._link
#
#     @property
#     def name(self):
#         return self._name
#
# class Action:
#     _path: Path
#     _sub_action: list
#
#     def __init__(self, path, sub_action=None):
#         _path = path
#         _sub_action = sub_action if sub_action is not None else []
#
#     @property
#     def link(self):
#         return self._path.link
#
#     @property
#     def text(self):
#         return self._path.name
#
#     @property
#     def sub_action(self):
#         return self._sub_action
#
# class NavigationStack:
#     _path_list: list
#
#     def __init__(self):
#         _path_list = [Path('/', popable=False)]
#
#     def push(self, new_route, popable=True):
#         self._path_list.append(new_route)
#
#     def pop(self):
#         path = self._path_list[-1]
#         if path.can_pop:
#             self._path_list.pop()
#
#     def maybe_pop(self):
#         path = self._path_list[-1]
#         if path.may_pop:
#             self._path_list.pop()
#
# # получает на вход массив путей и последовательно применяет пути для получения навигационного стэка
# # массив путей является разбитой по слэшам строкой
# # которая в свою очередь была получена из кнопки диалога (InlineButton)
# # KeyboardButton используется для ввода каких-то данных, но должен каким-то образом включать путь, который до этого существовал
# class NavigationManager:
#     AVAILABLE_COMMANDS = [
#         Action(
#             link='/about',
#             text='О боте',
#             sub_action=[
#                 Action(
#                     link='/author',
#                     text='Об авторах',
#                 ),
#                 Action(
#                     link='/version',
#                     text='Техническая информация',
#                 ),
#                 Action(
#                     link='/code',
#                     text='Об открытом коде',
#                 )
#             ]
#         ),
#         Action(
#             link='/art',
#             text='Сделать арт',
#             sub_action=[
#                 Action(
#                     link='/avatar',
#                     text='Взять фото профиля'
#                 )
#             ]
#         ),
#         Action(
#             link='/subscribe',
#             text='Подписаться',
#         ),
#         Action(
#             link='/about_ticker',
#             text='Про тикер',
#         ),
#         Action(
#             link='/about_date',
#             text='Про дату',
#         ),
#         Action(
#             link='/help',
#             text='Помощь',
#         ),
#     ]
#
#     navigator: NavigationStack
#
#     def generate_reply_keyboard(current_action: Action) -> types.ReplyKeyboardMarkup:
#         keyboard = types.ReplyKeyboardMarkup()
#         for el in current_action.sub_action:
#             keyboard.add(types.KeyboardButton(text=el))
#
#         return keyboard
#
#     def push(self):
#
