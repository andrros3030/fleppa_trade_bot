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
        self._rate = 0
        if user_id % 100 == 0:
            self._user_totem = 'Баффет'
            self._rate = 0.01
        elif user_id % 100 == 1:
            self._user_totem = 'Великая Наба'
            self._rate = 0.01
        elif user_id % 100 <= 60:
            self._user_totem = 'Хомячок'

    @property
    def totem(self):
        """
        :return: тотем пользователя
        """
        return self._user_totem

    def __str__(self):
        return f'Вы {self.totem}! Так себя назвать могут только {self._rate * 100}% пользователей 🔥'
