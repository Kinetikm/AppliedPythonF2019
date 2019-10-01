import json


def json_data(json_file, cod):
    file = open(json_file, 'r', encoding=cod)
    data = json.load(file)
    file.close()
    return data
