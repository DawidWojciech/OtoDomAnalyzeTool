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
                self.generate_marker_on_map(offers[0]).add_to(self.map)
            else:
                marker_cluster = MarkerCluster()
                for offer in offers:
                    marker_cluster.add_child(self.generate_marker_on_map(offer))
                self.map.add_child(marker_cluster)

    def generate_map(self):
        self.map.save(self.map_file)

    def create_data_with_coordinates(self):

        data = get_data_from_json_file(self.data_file)
        for offer in data:
            offer.update({"coordinates": self.get_coordinates_of_location(offer['location'])})

        return data

    def generate_marker_on_map(self, offer):

        if offer['property_type'] == 'Dom':
            marker = self.generate_marker_for_home(offer)
        elif offer['property_type'] == 'Działka':
            marker = self.generate_marker_for_building_plot(offer)

        return marker

    def generate_html_dependly_of_property_type(self, offer):

        if offer['property_type'] == 'Dom':
            html = self.generate_html_for_house(offer)
        elif offer['property_type'] == 'Działka':
            html = self.generate_html_for_building_plot(offer)

        return html

    @staticmethod
    def generate_html_for_house(offer):
        html = f"<b>Typ nieruchomości:</b> {offer['property_type']}<br>" \
               f"<b>Cena:</b> {offer['price']}<br>" \
               f"<b>Ilość pokoi:</b> {offer['rooms']}<br>" \
               f"<b>Powierzchnia domu:</b> {offer['area_1']}<br>" \
               f"<a href='{offer['link']}' target='_blank'>Link do oferty</a>"
        return html

    @staticmethod
    def generate_html_for_building_plot(offer):
        html = f"<b>Typ nieruchomości:</b> {offer['property_type']}<br>" \
               f"<b>Cena:</b> {offer['price']}<br>" \
               f"<b>Powierzchnia działki:</b> {offer['area_1']}<br>" \
               f"<a href='{offer['link']}' target='_blank'>Link do oferty</a>"
        return html

    def generate_marker_for_home(self, offer):
        html = self.generate_html_dependly_of_property_type(offer)
        icon = folium.map.Icon(color='blue', icon="glyphicon-home")
        return self.marker_object(offer, html, icon)

    def generate_marker_for_building_plot(self, offer):
        html = self.generate_html_dependly_of_property_type(offer)
        icon = folium.map.Icon(color='black', icon="glyphicon-tree-conifer")
        return self.marker_object(offer, html, icon)

    @staticmethod
    def marker_object(offer, html, icon):
        iframe = folium.IFrame(html=html, width=300, height=110)
        popup = folium.Popup(iframe, max_width=400)
        marker = folium.Marker([float(offer["coordinates"]["lat"]), float(offer["coordinates"]["long"])],
                               popup=popup, icon=icon)
        return marker
