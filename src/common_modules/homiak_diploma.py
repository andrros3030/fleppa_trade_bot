"""
NO PROJECT IMPORTS EXCEPT BASE_MODULES
"""
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from os import path


def diploma(name, totem):
    font_path = path.dirname(__file__) + '/../arial.ttf'
    url = "https://storage.yandexcloud.net/telegram-trade-bot/homyak_diploma.jpg"

    url1 = "https://storage.yandexcloud.net/telegram-trade-bot/fleppa_trademark.png"
    url1_image = requests.get(url1)
    image1 = Image.open(BytesIO(url1_image.content))

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

    txtwidth = drawer.textsize(totem, font=font)[0]
    drawer.text(((1600 - txtwidth) / 2, 1560), totem, fill="black", font=font)

    image.paste(image1, (397, 1584), image1.convert('RGBA'))

    # функция которая возвращает изображение, которое потом можно отправить сообщением
    my_stringIObytes = BytesIO()  # объект, который хранит данные изображения
    image.save(my_stringIObytes, format='jpeg')  # сохраняем изображение графика в my_stringIObytes в формате jpg
    my_stringIObytes.seek(0)  # не знаю че такое, наверное что-то важное
    return my_stringIObytes  # возвращаем объект хранящий изображение
