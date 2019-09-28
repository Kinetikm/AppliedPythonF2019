import json
import csv


def strt(x):
    return " " + str(x) + " "


def csv_process(filename, enc):
    reader = []
    with open(filename, encoding=enc) as e:
        tmp = csv.reader(e, delimiter="\t")
        for i in tmp:
            reader.append(list(map(strt, i)))
    return reader


def json_process(filename, enc):
    reader = []
    with open(filename, encoding=enc) as json_file:
        data = json.load(json_file)
        header = [i for i in data[0].keys()]
        header = list(map(strt, header))
        reader.append(header)
        for i in range(len(data)):
            row = [j for j in data[i].values()]
            row = list(map(strt, row))
            reader.append(row)
    return reader


def read_data(filename, enc):
    with open(filename, encoding=enc) as json_file:
        try:
            data = json.load(json_file)
        except ValueError:
            return csv_process(filename, enc)
    return json_process(filename, enc)
