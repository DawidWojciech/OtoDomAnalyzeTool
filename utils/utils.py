import json


def get_data_from_json_file(filepath: str):
    with open(filepath) as file:
        data = json.load(file)
        return data
