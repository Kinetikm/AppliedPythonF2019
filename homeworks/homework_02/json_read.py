import json


def is_json(file, enc):
    with open(file, 'r', encoding=enc) as f:
        try:
            json.load(f)
            return True
        except:
            return False


def json_read(file, enc):
    with open(file, 'r', encoding=enc) as f:
        table_data = []
        data = json.load(f)
        table_data.append([heads for heads in data[0].keys()])
        for dictionary in data:
            table_data.append([value for value in dictionary.values()])
        return table_data
