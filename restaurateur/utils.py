import requests
from django.conf import settings
from django.core.cache import cache
from geopy.distance import distance
from functools import partial


class PointError(Exception):
    pass


def fetch_coordinates(place):
    apikey = settings.YANDEX_GEO_API
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection'][
        'featureMember']
    if not places_found:
        raise PointError
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_distance_points(point_1, point_2):
    distance_points = None

    try:
        coordinates_point_1 = cache.get_or_set(point_1.replace(' ', '_'),
                                               partial(fetch_coordinates, point_1),
                                               100)
        coordinates_point_2 = cache.get_or_set(point_2.replace(' ', '_'),
                                               partial(fetch_coordinates, point_2),
                                               100)
    except PointError:
        return distance_points

    try:
        distance_points = distance(coordinates_point_1, coordinates_point_2).km
    except ValueError as e:
        print(f"Error distance {e}")
    return distance_points
