#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    n = len(list_of_lists[0])
    for row in list_of_lists:
        if len(row) != n:
            return None
    if n == 1:
        return list_of_lists[0][0]
    elif n > 1:
        det = 0
        step = 1
        for i in range(n):
            minor = [0] * (n - 1)
            for j in range(n - 1):
                minor[j] = [0] * (n - 1)
            for p in range(n - 1):
                for q in range(i):
                    minor[p][q] = list_of_lists[p + 1][q]
                for q in range(i, n - 1):
                    minor[p][q] = list_of_lists[p + 1][q + 1]
            det_min = calculate_determinant(minor)
            det += step * list_of_lists[0][i] * det_min
            step = -1 * step
        return det