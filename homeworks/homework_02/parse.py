import json
import csv


def read_data(f, enc, type_f):
    file = open(f, encoding=enc)
    res = []
    if type_f == 'json':
        data = json.load(file)
        res.append(list(data[0].keys()))
        for j in range(len(data)):
            if res[0] != list(data[j].keys()):
                raise
            l = []
            for x in data[j].values():
                if not isinstance(x, str):
                    l.append(str(x))
                else:
                    l.append(x)
            res.append(l)
    else:
        data = csv.reader(file, delimiter="\t")
        flag = False
        for i in data:
            if flag and len(i) != len(res[-1]):
                raise
            flag = True
            if i:
                res.append(i)
            else:
                raise
    return res


def print_data(data):
    size = []
    for j in range(len(data[0])):
        s = 0
        for k in range(len(data)):
            if s < len(data[k][j]):
                s = len(data[k][j])
        size.append(s)
    first = 5 * len(size) + sum(size) + 1
    print(first * '-')
    for i, line in enumerate(data):
        flag = '^' if i == 0 else '<'
        for j, value in enumerate(line):
            flag = '>' if j == 3 else flag
            line[j] = ("{:" + flag + str(size[j]) + "}").format(value)
        print("|  {}  |".format("  |  ".join(line)))
    print(first * '-')
