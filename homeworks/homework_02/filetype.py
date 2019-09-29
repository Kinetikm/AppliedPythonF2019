import json


def define_type(filename, coding):
    with open(filename, "r",  encoding=coding) as file:
        try:
            data = json.load(file)
        except:
            return 'Not json'
        else:
            head = data[0].keys()
            for line in data:
                if line.keys() != head:
                    return "Формат не валиден"
            return data
