import json
import csv


def read_file(path, enc):
    try:
        return read_json(path, enc)
    except json.decoder.JSONDecodeError:
        return read_tsv(path, enc)


def read_json(path, enc):
    with open(path, encoding=enc) as json_file:
        data_j = json.load(json_file)
    # making list_of_list from list_of_dicts
    list_of_lists = []
    titles = [title for title in data_j[0].keys()]
    list_of_lists.append(titles)
    for dct in data_j:
        line = []
        for key in dct.keys():
            line.append(str(dct[key]))
        list_of_lists.append(line)
    return list_of_lists


def read_tsv(path, enc):
    try:
        with open(path, encoding=enc) as csv_file:
            data = csv.reader(csv_file, delimiter='\t')
            output = []
            for row in data:
                output.append(row)
            return output
    except csv.Error:
        sys.exit("Формат не валиден")
