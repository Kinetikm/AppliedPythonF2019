import json
import csv


def open_json(file_name, encode):
    with open(file_name, encoding=encode) as file:
        data = json.load(file)
        return data


def open_tsv(file_name, encode):
    with open(file_name, encoding=encode) as file:
        table = []
        rd = csv.reader(file, delimiter="\t", quotechar="")
        for row in rd:
            table.append(row)
        return table


def ch_type(input_value, encode):
    try:
        value = open_json(input_value, encode)
        if value:
            return value
        value = open_tsv(input_value, encode)
        if value:
            return value
    except:
        raise FileNotFoundError
