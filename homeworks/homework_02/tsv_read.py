#!/usr/bin/env python
# coding: utf-8


def tsv_to_table(tsv_data):
    max_w = [0 for j in range(len(tsv_data[0]))]    # list of max column width
    for j in range(len(tsv_data[0])):    # j - column index
        for i in range(len(tsv_data)):    # i - row index
            if len(tsv_data[i][j]) > max_w[j]:
                max_w[j] = len(tsv_data[i][j])

    table_width = 1    # width of full table
    for x in max_w:
        table_width += x + 5

    print('-' * table_width)    # start of table - horisontal line
    for i in range(len(tsv_data)):
        print('|', end='')
        for j in range(len(tsv_data[0])):
            if (i == 0):
                print('{:^{width}}'.format(tsv_data[i][j], width=max_w[j] + 4), end='|')
            elif (j == len(tsv_data[0]) - 1):
                print('{:>{width}}  '.format(tsv_data[i][j], width=max_w[j] + 2), end='|')
            else:
                print('  {:<{width}}'.format(tsv_data[i][j], width=max_w[j] + 2), end='|')
        print()
    print('-' * table_width)  # start of table - horisontal line
