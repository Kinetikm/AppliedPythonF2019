import csv


def tsv_data(tsv_file, cod):
    list_rows = []

    file = open(tsv_file, encoding=cod)
    reader = csv.reader(file)

    for row in reader:
        list_rows.append(row[0].split('\t'))

    return list_rows
