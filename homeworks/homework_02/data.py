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


def print_data(data):
    size = []
    i = len(data)
    m = len(data[0])
    indent = 3
    for j in range(l):
        s = 0
        for k in range(i):
            if s < len(data[k][j]):
                s = len(data[k][j])
        size.append(s + 2 * indent)
    s = sum(size) - (m - 1)
    print(s * '-')
    begin = ''
    for j in range(m):
        spaces = int((size[j] - len(data[0][j]) - 2) / 2)
        begin += '|' + spaces * ' ' + data[0][j] + spaces * ' '
    begin += '|'
    print(begin)
    spaces = 2
    for x in range(1, i):
        string = ''
        for j in range(m):
            last = size[j] - len(data[x][j]) - 2 * spaces
            if j != m - 1:
                string += '|' + spaces * ' ' + data[x][j] + last * ' '
            else:
                string += '|' + last * ' ' + data[x][j] + spaces * ' '
        string += '|'
        print(string)
    print(s * '-')
