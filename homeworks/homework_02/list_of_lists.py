import csv


def csv_list_of_lists(path, encoding_format):
    with open(file=path, mode='r', encoding=encoding_format) as d:
        input_text = csv.reader(d, delimiter='\t')
        a = []
        for line in input_text:
            a.append(line)
    return a


def json_to_list(data):
    lst = [[key for key in data[0]]]
    for dict_ in data:
        lst.append([dict_[key] for key in dict_])
    return lst
