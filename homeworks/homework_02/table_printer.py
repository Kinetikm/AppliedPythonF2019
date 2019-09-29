#!/usr/bin/env python
# coding: utf-8


import open_any_file as oaf


def table_print(file_name):
    prt_table(oaf.open_file(file_name))


def prt_table(table):
    keys = []
    for i in table[0].keys():
        keys.append(i)
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
    print(just_line)
