from texttable import Texttable as t
import re


def build_table(reader):
    for i in range(len(reader[0])):
        if len(reader[0]) != len(reader[i]):
            print("Формат не валиден")
            raise SystemExit
    x = t()
    flag = False
    lens = [0 for i in reader[0]]
    for row in reader:
        for i in range(len(row)):
            if len(row[i]) > lens[i]:
                lens[i] = len(row[i])
        if flag:
            x.add_row(row)
        if not flag:
            x.header(row)
        flag = True
    x.set_cols_align(['l' for i in range(len(reader[0])-1)] + ['r'])
    x.set_deco(x.BORDER | x.VLINES)
    x.set_chars(['-', '|', '-', '#'])
    x.set_cols_width(lens)
    return re.sub(r' ([0-9]+) \|\n', r'\1  |\n', x.draw())
