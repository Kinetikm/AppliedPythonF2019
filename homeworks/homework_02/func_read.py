import json
import csv


def read_data(f, enc, type_f):
    file = open(f, encoding=enc)
    result = []
    if type_f == 'json':
        data = json.load(file)
        result.append(list(data[0].keys()))
        i = len(data[0].keys()) - 1
        for j in range(i):
            m = []
            for x in data[j].values():
                if type(x) != str:
                    m.append(str(x))
                else:
                    m.append(x)
            result.append(m)
    else:
        data = csv.reader(file, delimiter="\t")
        for i in data:
            result.append(i)
    return result
