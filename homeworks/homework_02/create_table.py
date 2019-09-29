from texttable import Texttable
import re


def create_table(data):
    for i in range(len(data[0])):
        if len(data[0]) != len(data[i]):
            print("Формат не валиден")
            raise SystemExit
    table = Texttable()
    table.header(data[0])
    table.set_header_align(["c"] * len(data[0]))
    table.set_cols_align(["l"] * (len(data[0]) - 1) + ["r"])
    table.set_deco(table.BORDER | table.VLINES)
    table.set_chars(['-', '|', '-', '#'])
    row = [0] * len(data[0])
    for i in range(len(data[0])):
        for j in range(len(data)):
            if row[i] < len(str(data[j][i])):
                row[i] = len(str(data[j][i]))
    table.set_cols_width(row)
    for i in range(1, len(data)):
        table.add_row(data[i])
    return re.sub(r' ([0-9]+) \|\n', r'\1  |\n', table.draw())
