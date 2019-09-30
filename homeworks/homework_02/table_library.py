#!/usr/bin/env python
# coding: utf-8


def frame_print(strings, columns):
    width = []
    for i in range(len(columns)):
        width.append(len(max(columns[i], key=len)))

    sum_width = sum(width) + 4 * len(columns) + len(columns) + 1
    print(unicode('-' * sum_width, "utf-8"))

    for j in range(len(strings)):
        my_str = ''
        for i in range(len(columns)):
            if j == 0:
                my_str += '|' + strings[j][i].center(width[i] + 4, ' ')
            else:
                if i != (len(columns) - 1):
                    my_str += '|' + '  ' + strings[j][i].ljust(width[i] + 4 - 2, ' ')
                else:
                    my_str += '|' + strings[j][i].rjust(width[i] + 4 - 2, ' ') + '  '

        my_str += '|'
        print(my_str)
    print('-' * sum_width)
