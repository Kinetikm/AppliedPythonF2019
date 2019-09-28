import sys
import json

# Ваши импорты
import os
import csv

if __name__ == '__main__':
    filename = sys.argv[1]

# Ваш код


def isjson(path, enc):
    try:
        with open(path, encoding=enc) as f:
            d = json.load(f)
    except json.decoder.JSONDecodeError:
        return False
    else:
        return True


def read_file(path, enc)->list:
    A = []
    if isjson(path, enc):
        with open(path, encoding=enc) as f:
            d = json.load(f)
        A.append(list(d[0].keys()))
        for line in d:
            A.append(list(line.values()))
        A = [list(map(str, item)) for item in A]
    else:
        with open(path, encoding = enc) as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            for row in tsvreader:
                A.append(row)
    return(A)

path = filename

if not os.path.exists(path):
    print('Файл не валиден')
else:
    encoding = ['utf8', 'utf16', 'cp1251']
    correct_encoding = ''
    for enc in encoding:
        try:
            open(path, encoding=enc).read()
        except (UnicodeDecodeError, LookupError, UnicodeError):
            # print('Формат не валиден')
            pass
        else:
            correct_encoding = enc
            A = read_file(path, correct_encoding)
            break

    B = [""]*len(A[0])
    for line in A:
        for i in range(len(A[0])):
            if len(line[i]) > len(B[i]):
                B[i] = line[i]

    B = [len(i) for i in B]
    for i, w in enumerate(A[0]):
        A[0][i] = w.center(B[i])

    for line in A[1:]:
        for i, w in enumerate(line[:-1]):
            line[i] = w.ljust(B[i])
        line[-1] = line[-1].rjust(B[-1])

    s = '-'*(sum(B) + 5*len(A[1]) + 1)
    print(s)
    for line in A:
        ss = '|  ' + '  |  '.join(line) + '  |'
        print(ss)
    print(s)
