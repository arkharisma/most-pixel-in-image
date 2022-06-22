from PIL import Image
import numpy
import requests
import json
import sys


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
            key = str(r) + "-" + str(g) + "-" + str(b)
            if key in colorDict:
                colorDict[key] += 1
            else:
                colorDict[key] = 1


def sort_color_dictionary(sourceDictionary):
    return sorted(sourceDictionary.items(), key=lambda item: item[1], reverse=True)


def fetch_color_detail(colorKey):
    url = "https://www.thecolorapi.com/id?format=json&rgb="
    r, g, b = colorKey.split('-')
    url = url + "rgb(" + r + "," + g + "," + b + ")"
    res = requests.get(url)
    response = json.loads(res.text)
    return response["hex"]["value"], response["name"]["value"].lower()


def grouping_color(colors):
    for key, value in colors[:50]:
        hexValue, colorName = fetch_color_detail(key)
        if colorName in mostColor:
            mostColor[colorName]["details"].append({
                "hex_code": hexValue,
                "count": value
            })
            mostColor[colorName]["total"] += value
        else:
            mostColor[colorName] = {
                "details": [{
                    "hex_code": hexValue,
                    "count": value
                }],
                "total": value
            }


image = get_image(sys.argv[1])
rgb_counter(image)
sortedColor = sort_color_dictionary(colorDict)
grouping_color(sortedColor)
for key, value in mostColor.items():
    print(key + ": " + str(value["total"]) + ' times')
    print("details: ")
    for val in value["details"]:
        print(val["hex_code"] + ": " + str(val["count"]) + " times")
    print()
