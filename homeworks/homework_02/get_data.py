import json
import csv


def get_tsv_data_as_list(filename):
    result = []
    tsv_data = csv.reader(filename, delimiter="\t")
    for line in tsv_data:
        result.append(line)
    return result


def get_json_data_as_list(filename):
    try:
        json_data = json.load(filename)
        result = []
        columns_row = list(json_data[0].keys())
        result.append(columns_row)
        for item_list in json_data:
            row = list()
            for key_dict in item_list:
                row.append(item_list[key_dict])
            result.append(row)
        return result
    except json.JSONDecodeError:
        return None
