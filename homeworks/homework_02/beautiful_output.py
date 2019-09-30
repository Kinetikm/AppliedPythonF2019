#!/usr/bin/env python
# coding: utf-8


def lenth(info, num_col):
    info_length = [[len(str(item)) for item in line] for line in info]
    widths = [0 for _ in range(num_col)]
    for line in info_length:
        for i in range(num_col):
            if widths[i] < line[i]:
                widths[i] = line[i]
    return widths


def create_field(info, num_col):
    n_sp = 2
    header = info[0]
    lines = info[1:]
    col_w = lenth(info, num_col)
    del_str = '-'*(sum(col_w) + n_sp*2*num_col + num_col + 1)

    h = '|'
    for i in col_w:
        h += '{space}{{:^{widht}}}{space}|'.format(space=' '*n_sp, widht=i)

    r = '|'
    for i in col_w[:len(col_w)-1]:
        r += '{space}{{:<{widht}}}{space}|'.format(space=' '*n_sp, widht=i)
    r += '{space}{{:>{widht}}}{space}|'.format(space=' '*n_sp, widht=col_w[-1])

    print(del_str)
    print(h.format(*header))
    for line in lines:
        print(r.format(*line))
    print(del_str)
