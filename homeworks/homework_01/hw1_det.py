#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    if len(list_of_lists) == 0 or len(list_of_lists) != len(list_of_lists[0]):
        return None
    elif len(list_of_lists) == 1:
        return list_of_lists[0][0]
    elif len(list_of_lists) == 2:
        return list_of_lists[0][0] * list_of_lists[1][1] - list_of_lists[0][1] * list_of_lists[1][0]
    else:
        det = 0
        minor = 1
        for i in range(len(list_of_lists)):
            m1 = []
            for j in range(1, len(list_of_lists)):
                m2 = []
                for k in range(0, len(list_of_lists)):
                    if k != i:
                        m2.append(list_of_lists[j][k])
                m1.append(m2)

            det += list_of_lists[0][i] * minor * calculate_determinant(m1)
            minor = -minor
    return det
