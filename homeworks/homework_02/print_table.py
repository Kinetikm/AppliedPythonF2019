#!/usr/bin/env python
# coding: utf-8


import read_json
import read_tsv
import get_type
import analyse_encode


def table_print(file):
    encode = analyse_encode.find_encode(file)
    if encode is not None:
        if get_type.type_of_file(file) == "json":
            return prt_table(read_json.json_reader(file, encode))
            # если файл типа json
        elif get_type.type_of_file(file) == "tsv":
            return prt_table(read_tsv.tsv_reader(file, encode))
            # если файл типа tsv
        else:
            print("Файл не валиден")
            return None
    else:
        print("Формат не валиден")
        return None


def prt_table(table):
    keys = []
    for name in table[0].keys():
        keys += [name]
    max_len = [max([len(max([key, tmp[key]], key=len)) for tmp in table])
               for key in table[0].keys()]
    one_line = "-" * (sum(max_len) + 5 * len(max_len) + 1)
    titles = "|  " + "  |  ".join(
        j.center(m) for j, m in zip(keys, max_len)) + "  |"
    main_inf = ["|  " + "  |  ".join(
        tmp[j].ljust(m) for j, m in zip(keys[:3], max_len)) + "  |  " + tmp[
                    keys[-1]].rjust(max_len[-1]) + "  |" for tmp in table]
    print(one_line)
    print(titles)
    for i in main_inf:
        print(i)
    print(one_line)
