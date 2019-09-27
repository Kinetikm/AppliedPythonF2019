import sys
import json
import csv


def get_list_from_dict(list_of_dicts: list) -> list:
    """[INPUT]: list_of_dicts - [{}, {}, ..]
       [RETURN]: list of lists, where list_of_lists[0] - dict.keys
                 list_of_lists[1:] - value for each key
       [EXAMPLE]: list_of_dicts = [{A: a, B: b, C: c}, {A: d, B: e, C: f}]
                  list_of_lists = [[A, B, C], [a, b, c], [d, e, f]]
    """
    list_of_lists = []
    titles = [title for title in list_of_dicts[0].keys()]
    list_of_lists.append(titles)
    for dct in list_of_dicts:
        line = []
        for key in dct.keys():
            line.append(str(dct[key]))
        list_of_lists.append(line)
    return list_of_lists


def read_json(filename, enc):
    with open(filename, encoding=enc) as json_file:
        data = json.load(json_file)
    list_from_dict = get_list_from_dict(data)
    return list_from_dict


def read_tsv(filename, enc):
    try:
        with open(filename, encoding=enc) as csvfile:
            data = csv.reader(csvfile, delimiter='\t')
            output = []
            for row in data:
                output.append(row)
            return output
    except csv.Error:
        sys.exit("Формат не валиден")


def read_file(filename, enc):
    try:
        return read_json(filename, enc)
    except json.decoder.JSONDecodeError:
        return read_tsv(filename, enc)
    except:
        sys.exit("Формат не валиден")
