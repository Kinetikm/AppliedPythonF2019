import csv


def get_data_from_tsv(filename, encoding):
    list_of_data = []
    with open(filename, 'r', encoding=encoding) as tsv_file:
        data = csv.reader(tsv_file, delimiter="\t")
        for i in data:
            list_of_data.append(i)
    return list_of_data
