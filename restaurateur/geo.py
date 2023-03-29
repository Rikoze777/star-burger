import requests
from locations.models import Location
from django.conf import settings
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from urllib.error import HTTPError


class LocationError(TypeError):
    def __init__(self, text):
        self.txt = text


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        raise LocationError('Введен некорректный адрес')

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_coordinates(order_address):
    try:
        location = Location.objects.get(address=order_address)
        lon = location.lon
        lat = location.lat
    except Location.DoesNotExist:
        try:
            lon, lat = fetch_coordinates(
                settings.YANDEX_API_KEY,
                order_address,
            )
        except KeyError as Er:
            lon, lat = None, None
        except HTTPError as Er:
            lon, lat = None, None
        Location.objects.get_or_create(
                query_date=datetime.now(),
                defaults={
                'address': order_address,
                'lon': lon,
                'lat': lat,
                }
            )
    order_coordinates = (lon, lat)
    return order_coordinates