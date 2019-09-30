#!/usr/bin/env python
# coding: utf-8


import raw_input as op


def print_t(file_name):
    form_t(op.raw_input(file_name))


def form_t(table):
    list = []
    for i in table[0].keys():
        keys.append(i)
    max_len = [max([len(max([key, tmp[key]], key=len)) for tmp in table])
               for key in table[0].keys()]
    minusl = "-" * (sum(max_len) + 5 * len(max_len) + 1)
    headlines = "|  " + "  |  ".join(
        j.center(m) for j, m in zip(keys, max_len)) + "  |"
    core = ["|  " + "  |  ".join(
        tmp[j].ljust(m) for j, m in zip(keys[:3], max_len)) + "  |  " + tmp[
                    keys[-1]].rjust(max_len[-1]) + "  |" for tmp in table]
    print(minusl)
    print(headlines)
    for i in core:
        print(i)
    print(minusl)
