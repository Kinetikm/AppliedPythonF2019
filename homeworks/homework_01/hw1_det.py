#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    det = 1
    for i in range(len(list_of_lists)):
        if len(list_of_lists[i]) != len(list_of_lists):
            return None
    for i in range(len(list_of_lists)):
        imax = i
        cs = 1
        for j in range(i+1, len(list_of_lists)):
            if abs(list_of_lists[j][i]) > abs(list_of_lists[imax][i]):
                imax = j
        list_of_lists[i], list_of_lists[imax] = list_of_lists[imax], list_of_lists[i]
        if imax != i:
            cs = cs * (-1)
        for j in range(i+1, len(list_of_lists)):
            coef = -list_of_lists[j][i] / list_of_lists[i][i]
            for q in range(len(list_of_lists) - 1, i - 1, -1):
                list_of_lists[j][q] += coef * list_of_lists[i][q]
        det *= cs * list_of_lists[i][i]
    return det
