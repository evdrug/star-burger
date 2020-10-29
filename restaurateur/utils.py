import requests
from django.conf import settings
from django.core.cache import cache
from geopy.distance import distance


def fetch_coordinates(place):
    apikey = settings.YANDEX_GEO_API
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection'][
        'featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def distance_points(point_1, point_2):
    coordinates_point_1 = cache.get_or_set(point_1.replace(' ', '_'),
                                           fetch_coordinates(point_1),
                                           100)
    coordinates_point_2 = cache.get_or_set(point_2.replace(' ', '_'),
                                           fetch_coordinates(point_2),
                                           100)
    coordinates = f"{coordinates_point_1[0]}/{coordinates_point_1[1]}_" \
                  f"{coordinates_point_2[0]}/{coordinates_point_2[1]}"
    distance_cache = cache.get_or_set(coordinates,
                                      distance(coordinates_point_1,
                                               coordinates_point_2).km, 100)
    return distance_cache
