import folium
from geopy.geocoders import Nominatim

from utils.utils import get_data_from_json_file


class MapGenerator:

    def __init__(self, data_file: str, map_file: str):
        self.data_file = data_file
        self.map_file = map_file
        self.map = folium.Map(location=[51.1079, 17.0385])
        self.data = self.create_data_with_coordinates()

    def generate_markers(self):

        for offer in self.data:
            popup_data = f"<b>{offer['title']}</b>\n" \
                         f"{offer['rooms']}\n" \
                         f"{offer['house_area']}\n" \
                         f"{offer['property_type']}\n" \
                         f"<a href='{offer['link']}'>link</a>"
            folium.Marker([float(offer["coordinates"]["lat"]), float(offer["coordinates"]["long"])],
                          popup=popup_data
                          ).add_to(self.map)

    def generate_map(self):
        self.map.save(self.map_file)

    def create_data_with_coordinates(self):

        data = get_data_from_json_file(self.data_file)
        for offer in data:
            offer.update({"coordinates": self.get_coordinates_of_location(offer['location'])})

        return data

    @staticmethod
    def get_coordinates_of_location(location: str) -> dict:

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
