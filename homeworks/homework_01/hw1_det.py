#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    for lst in list_of_lists:
        if len(list_of_lists) != len(lst):
            return None
    if len(list_of_lists) == 1:
        return list_of_lists[0][0]
    elif len(list_of_lists) == 2:
        a = list_of_lists[0][0] * list_of_lists[1][1]
        b = list_of_lists[0][1] * list_of_lists[1][0]
        return a - b
    else:
        det = 0
        for i in range(len(list_of_lists)):
            a = []
            for j in range(1, len(list_of_lists)):
                b = []
                for k in range(len(list_of_lists[j])):
                    if k == i:
                        continue
                    b.append(list_of_lists[j][k])
                a.append(b)
            det += ((-1)**i) * list_of_lists[0][i] * calculate_determinant(a)
        return det
