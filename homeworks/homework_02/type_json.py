import json


def define_json(file, enc):
    with open(file, 'r', encoding=enc) as f:
        try:
            json.load(f)
            return True
        except:
            return False


def json_tab(file, enc):
    with open(file, 'r', encoding=enc) as f:
        table = []
        data = json.load(f)
        titles = []
        for title in data[0].keys():
            titles.append(title)
        table.append(titles)
        for dict in data:
            val_list = []
            for val in dict.values():
                val_list.append(val)
            table.append(val_list)
        return table
