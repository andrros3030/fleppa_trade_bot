from PIL import Image
from urllib.request import urlopen

url = "http://risovach.ru/upload/2014/02/mem/muzhik-bleat_43233947_orig_.jpg"

image = Image.open(urlopen(url))
image.show()