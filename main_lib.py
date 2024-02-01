import sys
from io import BytesIO
import requests
from PIL import Image
import pprint


def get_spn(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])
    env = toponym['boundedBy']['Envelope']
    l, b = env['lowerCorner'].split(" ")
    r, t = env['upperCorner'].split(" ")
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    span = f'{dx},{dy}'
    return ll, span


def get_map(place):
    ll, spn = get_spn(place)
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": "map",
        "pt": "{0},pm2dgl".format(ll)

    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"

    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()


if __name__ == '__main__':
    toponym_to_find = " ".join(sys.argv[1:])
    if not toponym_to_find:
        toponym_to_find = input('Введите объект для поиска: ')
    get_map(toponym_to_find)
