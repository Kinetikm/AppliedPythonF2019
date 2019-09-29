import json
import csv


def get_tsv_data_as_list(file):
    try:
        result_list = []
        tsv_data = csv.reader(file, delimiter="\t")
        for sub_list in tsv_data:
            result_list.append(list(sub_list))
        return result_list
    except csv.Error:
        return None


def get_json_data_as_list(file):
    try:
        json_data = json.load(file)
        list_data = []
        column_row = list(json_data[0].keys())
        list_data.append(column_row)
        for item_list in json_data:
            row = list()
            for key_dict in item_list:
                row.append(item_list[key_dict])
            list_data.append(row)
        return list_data
    except json.JSONDecodeError:
        return None
