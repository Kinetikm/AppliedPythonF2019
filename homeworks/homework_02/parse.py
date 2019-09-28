import json
import csv


def read_data(f, enc, type_f):
    file = open(f, encoding=enc)
    res = []
    if type_f == 'json':
        data = json.load(file)
        res.append(list(data[0].keys()))
        i = len(data[0].keys()) - 1
        for j in range(i):
            l = []
            for x in data[j].values():
                if type(x) != str:
                    l.append(str(x))
                else:
                    l.append(x)
            res.append(l)
    else:
        data = csv.reader(file, delimiter="\t")
        for i in data:
            res.append(i)
    return res


def print_data(data):
    size = []
    i = len(data)
    l = len(data[0])
    indent = 3
    for j in range(l):
        s = 0
        for k in range(i):
            if s < len(data[k][j]):
                s = len(data[k][j])
        size.append(s + 2 * indent)
    s = sum(size) - (l - 1)
    print(s * '-')
    head = ''
    for j in range(l):
        spaces = int((size[j] - len(data[0][j]) - 2) / 2)
        head += '|' + spaces * ' ' + data[0][j] + spaces * ' '
    head += '|'
    print(head)
    spaces = 2
    for x in range(1, i):
        string = ''
        for j in range(l):
            last = size[j] - len(data[x][j]) - 2 * spaces
            if j != l - 1:
                string += '|' + spaces * ' ' + data[x][j] + last * ' '
            else:
                string += '|' + last * ' ' + data[x][j] + spaces * ' '
        string += '|'
        print(string)
    print(s * '-')
