"""
NO PROJECT IMPORTS IN THIS FILE
"""


class Totem:
    """
    Класс для выбора тотема пользователя
    Пока что логика выдаёт тотемы по шансам, но в будущем возможно, что будет передаваться минус на пульсе)
    """
    def __init__(self, user_id):
        self._user_totem = ''
        last_two = user_id % 100
        if last_two == 0:  # 1% chance
            self._user_totem = 'Уоррен Баффет'
            rate = 0.01
            self._sticker = '🔥🔥🔥'
        elif last_two == 1:  # 1% chance
            self._user_totem = 'Великая Наба'
            rate = 0.01
            self._sticker = '🔥🔥🔥'
        elif last_two <= 5:  # 3% chance
            self._user_totem = 'квал с черешней'  # TODO
            rate = 0.03
            self._sticker = '😬'  # TODO
        elif last_two <= 15:  # 10% chance
            self._user_totem = 'волк'
            rate = 0.1
            self._sticker = '🐺'
        elif last_two <= 45:  # 30% chance
            self._user_totem = 'пульсянин'
            rate = 0.3
            self._sticker = '🤘'
        else:  # 55% chance
            self._user_totem = 'хомячок обыкновенный'
            rate = 0.55
            self._sticker = '🌚'
        self._rate = int(rate * 100)


    @property
    def totem(self):
        """
        :return: тотем пользователя капслоком для вывода в изображении
        """
        return self._user_totem.upper()

    def __str__(self):
        return f'Вы {self._user_totem} {self._sticker}!\nТак себя назвать могут только {self._rate}% пользователей'
