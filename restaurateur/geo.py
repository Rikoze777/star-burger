import requests
from locations.models import Location
from django.conf import settings
from datetime import datetime


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
        return None, None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_coordinates(order_address):
    try:
        location = Location.objects.get(address=order_address)
        lon = location.lon
        lat = location.lat
    except Location.DoesNotExist:
        lon, lat = fetch_coordinates(
            settings.YANDEX_API_KEY,
            order_address,
        )
        if not lon and not lat:
            lon = 37.6156
            lat = 55.7522
        Location.objects.get_or_create(
            address=order_address,
            lon=lon,
            lat=lat,
            query_date=datetime.now()
        )
    order_coordinates = (lon, lat)
    return order_coordinates