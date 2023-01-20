from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen
import io


def diploma(name):
    url = "https://storage.yandexcloud.net/telegram-trade-bot/homyak_diploma.jpg"
    image = Image.open(urlopen(url))

    font = ImageFont.truetype("arial.ttf", 75)
    drawer = ImageDraw.Draw(image)
    txtwidth = drawer.textsize(name, font=font)[0]
    drawer.text(((1600 - txtwidth) / 2, 1070), name, fill="black", font=font)

    # функция которая возвращает изображение, которое потом можно отправить сообщением
    my_stringIObytes = io.BytesIO()  # объект, который хранит данные изображения
    image.save(my_stringIObytes, format='jpeg')  # сохраняем изображение графика в my_stringIObytes в формате jpg
    my_stringIObytes.seek(0)  # не знаю че такое, наверное что-то важное
    return my_stringIObytes  # возвращаем объект хранящий изображение
