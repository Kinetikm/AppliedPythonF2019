#!/usr/bin/env python
# coding: utf-8


import open_data as op


def print_table(file_name):
    prt_table(op.open_data(file_name))


def prt_table(table):
    keys = []
    for i in table[0].keys():
        keys.append(i)
    #keys = [i for i in table[0].keys()]
    max_len = [max([len(max([key, tmp[key]], key=len)) for tmp in table])
               for key in table[0].keys()]
    just_line = "-" * (sum(max_len) + 5 * len(max_len) + 1)
    titles = "|  " + "  |  ".join(
        j.center(m) for j, m in zip(keys, max_len)) + "  |"
    main_inf = ["|  " + "  |  ".join(
        tmp[j].ljust(m) for j, m in zip(keys[:3], max_len)) + "  |  " + tmp[
                    keys[-1]].rjust(max_len[-1]) + "  |" for tmp in table]
    print(just_line)
    print(titles)
    for i in main_inf:
        print(i)
    #[print(i) for i in main_inf]
    print(just_line)
    
