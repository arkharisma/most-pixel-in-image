from posixpath import split
from PIL import Image
import numpy
import requests
import json


colorDict = {}
mostColor = {}


def get_image(image_path):
    image = Image.open(image_path, "r").convert("RGB")
    width, height = image.size
    pixel_values = list(image.getdata())
    channels = 3
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values


def rgb_counter(image):
    for img in image:
        for i in img:
            r, g, b = i
            key = str(r) + '-' + str(g) + '-' + str(b)
            if key in colorDict:
                colorDict[key] += 1
            else:
                colorDict[key] = 1


def sort_color_dictionary(sourceDictionary):
    return sorted(sourceDictionary.items(), key=lambda item: item[1], reverse=True)


def fetch_color_detail(colorKey):
    url = 'https://www.thecolorapi.com/id?format=json&rgb='
    r, g, b = colorKey.split('-')
    url = url + 'rgb(' + r + ','+g+','+b+')'
    res = requests.get(url)
    response = json.loads(res.text)
    return response['hex']['clean'], response['hex']['value'], response['name']['value']


image = get_image("images/boly.png")
rgb_counter(image)
sortedColor = sort_color_dictionary(colorDict)
for key, value in sortedColor[:50]:
    cleanHex, hexValue, colorName = fetch_color_detail(key)
    mostColor[cleanHex] = {
        "hex_code": hexValue,
        "color_name": colorName,
        "count": value
    }
print(mostColor)