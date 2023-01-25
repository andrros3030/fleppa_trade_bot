from PIL import Image
from io import BytesIO
import requests


fleppa_watermark_url = 'https://storage.yandexcloud.net/telegram-trade-bot/fleppa_trademark.png'


def add_fleppa_wm(your_image, x, y):
    """
    :param your_image: фото, на которое фотошопиться вотермарка(стоит понимать, что оно должно быть в байтах)
    :param x: левая граница положения вотермарки
    :param y: верхняя граница положения вотермарки
    """
    fleppa_watermark = requests.get(fleppa_watermark_url).content
    fleppa_watermark_image = Image.open(BytesIO(fleppa_watermark))
    photo = BytesIO()
    photo_image = Image.open(your_image)
    photo_image.paste(fleppa_watermark_image, (x, y), fleppa_watermark_image.convert('RGBA'))
    photo_image.save(photo, format='jpeg')
    photo.seek(0)
    return photo
