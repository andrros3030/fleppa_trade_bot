from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen
import io


def diploma(name):
    url = "https://storage.yandexcloud.net/telegram-trade-bot/homyak_diploma.jpg"
    image = Image.open(urlopen(url))

    font = ImageFont.truetype("arial.ttf", 75)
    drawer = ImageDraw.Draw(image)
   # drawer.text((600, 1070), name, font=font, fill='black', align="center", anchor="mm")

    W = 1280 - 330
    H = 1170 - 1060
    _, _, w, h = drawer.textbbox((330, 1060), name, font=font)
    drawer.text(((W - w) / 2, (H - h) / 2), name, font=font, fill='black')

    # функция которая возвращает изображение, которое потом можно отправить сообщением
    my_stringIObytes = io.BytesIO()  # объект, который хранит данные изображения
    image.save(my_stringIObytes, format='jpeg')  # сохраняем изображение графика в my_stringIObytes в формате jpg
    my_stringIObytes.seek(0)  # не знаю че такое, наверное что-то важное
    return my_stringIObytes  # возвращаем объект хранящий изображение
