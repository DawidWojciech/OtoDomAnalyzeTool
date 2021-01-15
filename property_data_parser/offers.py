import json
from utils.utils import get_data_from_json_file


class OfferParser():
    def __init__(self, offer_file):
        self.offer_file = offer_file

    def group_offers_per_coordinates(self):
        offers = get_data_from_json_file(self.offer_file)
        locations_with_offers = {}

        for offer in offers:
            coordinates_key = f'{offer["coordinates"]["lat"], offer["coordinates"]["long"]}'
            if coordinates_key in locations_with_offers:
                if offer in locations_with_offers[coordinates_key]:
                    pass
                else:
                    locations_with_offers[coordinates_key].append(offer)
            else:
                locations_with_offers.update({coordinates_key: [offer]})

        return locations_with_offers

    def save_as_json(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.group_offers_per_coordinates(), file)

