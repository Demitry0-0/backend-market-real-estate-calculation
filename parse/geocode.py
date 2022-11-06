import math
from math import acos, sin, cos

import requests


def get_geocode(address) -> tuple:
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        return tuple()

    json_response = response.json()
    return tuple(map(float,
                     json_response['response']['GeoObjectCollection']['featureMember'][0][
                         "GeoObject"][
                         'Point'][
                         'pos'].split()[::-1]))


def get_distance(address1: str, address2: str):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = get_geocode(address1)[::-1]
    b_lon, b_lat = get_geocode(address2)[::-1]
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance
