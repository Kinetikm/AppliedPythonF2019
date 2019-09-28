from texttable import Texttable
import re


def draw_table(lst_of_lst):
    table = Texttable()
    header_align = ["c"] * len(lst_of_lst[0])
    cols_align = ["r"]
    for i in range(len(lst_of_lst[0])-1):
        cols_align.insert(0, "l")
    cols_width = [0] * len(lst_of_lst[0])
    for line in lst_of_lst:
        for i, val in enumerate(line):
            line[i] = str(line[i])
            if i != len(line) - 1:
                line[i] = ' ' + line[i] + ' '
            else:
                line[i] = ' ' + line[i] + ' '
    for line in lst_of_lst:
        for i, val in enumerate(line):
            if len(str(val)) > cols_width[i]:
                cols_width[i] = len(val)
    table.header(lst_of_lst[0])
    table.set_cols_width(cols_width)
    table.set_deco(Texttable.BORDER | Texttable.VLINES)
    table.set_cols_align(cols_align)
    table.set_header_align(header_align)
    table.set_chars(['-', '|', '-', '#'])
    for i in lst_of_lst[1:]:
        table.add_row(i)
    print(re.sub(r' ([0-9]+) \|\n', r'\1  |\n', table.draw()))
