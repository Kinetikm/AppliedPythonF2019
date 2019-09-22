#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    EPS = 1e-15
    z = len(list_of_lists)
    for i in range(z):
        if len(list_of_lists[i]) != z:
            return None
    det = 1
    for i in range(z):
        Max = i
        for j in range(i + 1, z):
            if abs(list_of_lists[j][i]) > abs(list_of_lists[Max][i]):
                Max = j
        if abs(list_of_lists[Max][i]) < EPS:
            return 0
        list_of_lists[i], list_of_lists[Max] = list_of_lists[Max], list_of_lists[i]
        if i != Max:
            det *= -1
        det *= list_of_lists[i][i]
        for j in range(i + 1, z):
            list_of_lists[i][j] /= list_of_lists[i][i]
        for j in range(z):
            if j != i and abs(list_of_lists[j][i]) > EPS:
                for k in range(i + 1, z):
                    list_of_lists[j][k] -= list_of_lists[i][k] * list_of_lists[j][i]
    return det



