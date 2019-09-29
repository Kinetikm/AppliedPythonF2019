import json


def parse_data(data):

    def _parse_json(d):
        try:
            json_data = json.loads(d)
        except json.JSONDecodeError:
            return 0, None
        if type(json_data) is not list or not len(json_data):
            return -1, None
        parsed_data = list()
        parsed_data.append(list(json_data[0].keys()))
        for json_object in json_data:
            if json_object is None:
                continue
            if list(json_object.keys()) != parsed_data[0]:
                return -1, None
            data_list = list(json_object.values())
            if len(data_list) != len(parsed_data[0]):
                return -1, None
            parsed_data.append(data_list)
        return 1, parsed_data

    def _parse_tsv(d):
        try:
            tsv_data = d.split("\n")
        except ValueError:
            return 0, None
        parsed_data = list()
        # заголовок
        string = tsv_data[0].split("\t")
        if string[0] is "":
            return -1, None
        parsed_data.append(string)
        # прочее
        for string in tsv_data[1:]:
            if string is "":
                continue
            data_list = string.split("\t")
            if len(data_list) != len(parsed_data[0]):
                return -1, None
            parsed_data.append(data_list)
        return 1, parsed_data

    parsed = _parse_json(data)
    if parsed[0] == 1:
        return parsed[1]
    elif parsed[0] == -1:
        return None
    parsed = _parse_tsv(data)
    if parsed[0] == 1:
        return parsed[1]
    elif parsed[0] == -1:
        return None
    return None
