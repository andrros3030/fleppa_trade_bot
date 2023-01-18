from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen

name = "Алексей"
surname = "Проверка"
xcv = " "
aboba = name + xcv + surname

url = "https://storage.yandexcloud.net/telegram-trade-bot/homyak_diploma.jpg"
image = Image.open(urlopen(url))

font = ImageFont.truetype("arial.ttf", 45)
drawer = ImageDraw.Draw(image)
drawer.text((600, 1100), aboba, font=font, fill='black')

image.show()