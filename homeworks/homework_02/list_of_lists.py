import csv


def csv_list_of_lists(path, codir):
    with open(file=path, mode='r', encoding=codir) as d:
        read = csv.reader(d, delimiter='\t')
        a = []
        for line in read:
            a.append(line)
    return a


def json_to_list(data):
    lst = []
    lst.append([key for key in data[0]])
    for dict_ in data:
        lst.append([dict_[key] for key in dict_])
    return lst
