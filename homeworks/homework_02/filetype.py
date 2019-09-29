import json


def define_type(filename, coding):
    with open(filename, "r",  encoding=coding) as file:
        try:
            data = json.load(file)
        except:
            return 'Not json'
    return data
