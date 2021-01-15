import json
from geopy.geocoders import Nominatim


def get_data_from_json_file(filepath: str):
    with open(filepath) as file:
        data = json.load(file)
        return data


def get_coordinates_of_location(location: str) -> str:
    geolocator = Nominatim(user_agent="propery_for_sale")
    geo_location = geolocator.geocode(location)

    if geo_location is not None:
        coordinates = {"lat": float(geo_location.latitude),
                       "long": float(geo_location.longitude)
                       }
    else:

        geo_location = geolocator.geocode(location.split(", ")[0])
        coordinates = {"lat": float(geo_location.latitude),
                       "long": float(geo_location.longitude)
                       }
    return coordinates
