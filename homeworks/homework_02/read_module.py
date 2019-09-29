import json
import csv


def readjson(filename, enc):
    with open(filename, encoding=enc) as fin:
        data = json.loads(fin.read())
    return data


def readtsv(filename, enc):
    with open(filename, 'r', encoding=enc) as fin:
        data = csv.reader(fin.readlines(), delimiter="\t")
    return list(data)
