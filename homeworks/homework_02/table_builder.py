#!/usr/bin/env python
# coding: utf-8


from other_methods import columns_len


def table_builder(data):
    col_len = columns_len(data)
    hyphens = '-' * (sum(col_len) + 4 * len(data[0]) + 5)
    print(hyphens)

    for lists in data[:1]:
        stri = '|'
        for num, single_string in enumerate(lists[:-1]):
            stri = ''.join([stri, (int((col_len[num] - len(
                str(single_string)) + 1) / 2) + 2) * ' ', str(
                single_string), (int((col_len[num] - len(
                    str(single_string))) / 2) + 2) * ' ', '|'])
        stri = ''.join([stri, (int((col_len[-1] - len(
                    str(lists[-1])) + 1) / 2) + 2) * ' ', str(
            lists[-1]), (int((col_len[-1] - len(
                str(lists[-1])) + 1) / 2) + 2) * ' ' + '|'])
        print(stri)
    for lists in data[1:]:
        stri = '|'
        for num, single_string in enumerate(lists[:-1]):
            stri = ''.join([stri, 2 * ' ', str(single_string), (
                    col_len[num] - len(str(single_string)) + 2) * ' ', '|'])
        stri = ''.join([stri, (col_len[-1] - len(str(
                    lists[-1])) + 2) * ' ', str(lists[-1]), 2 * ' ' + '|'])
        print(stri)
    print(hyphens)
