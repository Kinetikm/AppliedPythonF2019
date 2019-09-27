#!/usr/bin/env python
# coding: utf-8


def json_to_table(json_data):
    d_table = {}    # dictionary for column data: keys - names of columns
    max_d = {}    # dictionary for saving max date length in column

    for key in json_data[0]:    # creating empty lists for every column
        d_table[key] = []
        max_d[key] = 0

    for key in d_table:    # fill lists for every column & calculate max length
        max_d[key] = len(key)
        for json_dict in json_data:
            d_table[key] += [json_dict[key]]
            if (len(str(json_dict[key])) > max_d[key]):
                max_d[key] = len(json_dict[key])

    table_width = 1  # width of full table
    for key in max_d:
        table_width += max_d[key] + 3

    print('-' * table_width)    # start of table - horisontal line

    print('|', end='')
    for key in d_table:    # row with column names
        i = max_d[key]
        print('{:^{width}}'.format(key, width=i + 2), end='|')
    print()

    for j in range(len(json_data)):
        print('|', end='')
        for key in d_table:
            i = max_d[key]
            print('{:^{width}}'.format(d_table[key][j], width=i + 2), end='|')
        print()
    print('-' * table_width)
