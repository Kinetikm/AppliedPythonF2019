#!/usr/bin/env python
# coding: utf-8


def get_table(struct):
    try:
        res = ''
        headers = [i for i in struct[0]]
        if len(struct) < 2:
            lens, bound_len = get_max_cell_lens([headers])
            bound = "-" * (bound_len + len(lens) + 1)
            res += bound + '\n|'
            for i, col in enumerate(headers):
                res += '{:^{}}'.format("  " + col + "  ", lens[i]) + '|'
            return res + '\n' + "-" * (bound_len + len(lens) + 1)
        values = [[str(j[i]) for i in j] for j in struct]
        lens, bound_len = get_max_cell_lens([headers] + values)
        bound = "-" * (bound_len + len(lens) + 1)
        res += bound + '\n|'
        for i, col in enumerate(headers):
            res += '{:^{}}'.format("  " + col + "  ", lens[i]) + '|'
        res += '\n'
        for line in values:
            res += '|'
            for i, col in enumerate(line):
                len_cell = lens[i]
                if i < len(line) - 1:
                    res += '{:<{}}'.format("  " + col + "  ", len_cell) + '|'
                else:
                    res += '{:>{}}'.format("  " + col + "  ", len_cell) + '|'
            res += '\n'
        res += "-" * (bound_len + len(lens) + 1)
        return res
    except BaseException:
        return None


def get_max_cell_lens(table):
    lens = [0 for i in table[0]]
    line_len = 0
    for line in table:
        for i, col in enumerate(line):
            if lens[i] < len(col) + 4:
                line_len += len(col) + 4 - lens[i]
                lens[i] = len(col) + 4
    return lens, line_len
