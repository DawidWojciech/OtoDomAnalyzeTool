import folium
from folium.plugins import MarkerCluster

from utils.utils import get_data_from_json_file


class MapGenerator:

    def __init__(self, data_file: str, map_file: str):
        self.data_file = data_file
        self.map_file = map_file
        self.map = folium.Map(location=[51.1079, 17.0385])
        # self.data = self.create_data_with_coordinates()
        self.locations = get_data_from_json_file('parsed.json')

    def add_markers_to_map(self):

        for location, offers in self.locations.items():
            if len(offers) == 1:
                self.generate_marker(offers[0]).add_to(self.map)
            else:
                marker_cluster = MarkerCluster()
                for offer in offers:
                    marker_cluster.add_child(self.generate_marker(offer))
                self.map.add_child(marker_cluster)

    def generate_map(self):
        self.map.save(self.map_file)

    def create_data_with_coordinates(self):

        data = get_data_from_json_file(self.data_file)
        for offer in data:
            offer.update({"coordinates": self.get_coordinates_of_location(offer['location'])})

        return data

    def generate_marker(self, offer):
        html = f"<b>Typ nieruchomości:</b> {offer['property_type']}<br>" \
               f"<b>Cena:</b> {offer['price']}<br>" \
               f"<b>Ilość pokoi:</b> {offer['rooms']}<br>" \
               f"<b>Powierzchnia domu:</b> {offer['area_1']}<br>" \
               f"<a href='{offer['link']}' target='_blank'>Link do oferty</a>"
        iframe = folium.IFrame(html=html, width=300, height=110)
        popup = folium.Popup(iframe, max_width=400)
        marker = folium.Marker([float(offer["coordinates"]["lat"]), float(offer["coordinates"]["long"])],
                               popup=popup)

        return marker
