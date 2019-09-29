import csv
import json
import sys


def read_tsv(path, enc) -> list:
    A = []
    with open(path, 'r', encoding=enc) as file:
        tsvreader = csv.reader(file, delimiter="\t")
        for row in tsvreader:
            A.append(row)
    return(A)


def read_json(path, enc) -> list:
    A = []
    with open(path, 'r', encoding=enc) as file:
        d = json.load(file)
    A.append(list(d[0].keys()))
    for line in d:
        A.append(list(line.values()))
    A = [list(map(str, item)) for item in A]
    return(A)


def read_file(filename, enc):
    try:
        return read_json(filename, enc)
    except json.decoder.JSONDecodeError:
        return read_tsv(filename, enc)
    except:
        sys.exit("Формат не валиден")
