"""
NO PROJECT IMPORTS EXCEPT BASE_MODULES
"""
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from os import path


def diploma(name):
    font_path = path.dirname(__file__) + '/../arial.ttf'
    url = "https://storage.yandexcloud.net/telegram-trade-bot/homyak_diploma.jpg"
    try:
        url_image = requests.get(url)
        image = Image.open(BytesIO(url_image.content))
    except Exception:
        raise Exception(f"Can't open image by passed URL {url}")
    try:
        font = ImageFont.truetype(font_path, 75)
    except Exception:
        raise Exception(f"Can't open font in location {font_path}")

    drawer = ImageDraw.Draw(image)
    txtwidth = drawer.textsize(name, font=font)[0]
    drawer.text(((1600 - txtwidth) / 2, 1070), name, fill="black", font=font)

    # функция которая возвращает изображение, которое потом можно отправить сообщением
    my_stringIObytes = BytesIO()  # объект, который хранит данные изображения
    image.save(my_stringIObytes, format='jpeg')  # сохраняем изображение графика в my_stringIObytes в формате jpg
    my_stringIObytes.seek(0)  # не знаю че такое, наверное что-то важное
    return my_stringIObytes  # возвращаем объект хранящий изображение
