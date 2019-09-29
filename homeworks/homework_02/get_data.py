import json
import csv


def get_tsv_data_as_list(file):
    result = []
    tsv_data = csv.reader(file, delimiter="\t")
    for line in tsv_data:
        result.append(line)
    return result


def get_json_data_as_list(file):
    try:
        json_data = json.load(file)
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
