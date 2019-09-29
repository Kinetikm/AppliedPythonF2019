from check_module import get_format, get_enc
from read_module import readjson, readtsv


def get_matrix(filename):
    form = get_format(filename)
    enc = get_enc(filename)
    if form == 'tsv':
        lines = readtsv(filename, enc)
        return lines
    elif form == 'json':
        lines = readjson(filename, enc)
        matrix = list()
        keys = list()
        for key in lines[0].keys():
            keys.append(str(key))
        matrix.append(keys)
        for line in lines:
            d = list()
            for key in keys:
                d.append(str(line[key]))
            matrix.append(d)
        return matrix


def create_table(lines):
    d = list()
    max = 0
    for i in range(len(lines[0])):
        for j in range(len(lines)):
            if max < len(lines[j][i]):
                max = len(str(lines[j][i]))
        d.append(max)
        max = 0
    outputlist = list()
    z = '-'*(sum(d)+6+(len(d)-1)*5)
    outputlist.append(z)
    c = '|'
    for i in range(len(lines[0])):
        index = (d[i]+4 - len(lines[0][i]))
        c += ' ' * (index // 2)
        c += lines[0][i]
        c += ' ' * (d[i]+4 - len(lines[0][i]) - index//2)
        c += '|'
    outputlist.append(c)
    for line in lines[1:]:
        c = '|  '
        for i in range(len(line)):
            if i != len(line)-1:
                c += line[i]
                c += ' ' * (d[i] - len(line[i]))
                c += '  |  '
            else:
                c += ' '*(d[i]-len(line[i]))
                c += line[i]
                c += '  |'
        outputlist.append(c)
    outputlist.append(z)
    return outputlist
