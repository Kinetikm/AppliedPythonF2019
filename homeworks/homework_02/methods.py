def json_to_list(data):
    json_list = []
    json_list.append(list(data[0].keys()))
    for item in data:
        json_list.append(list(item.values()))
    return json_list


def tsv_to_list(data):
    tsv_list = [item.split('\t') for item in data]
    return tsv_list
