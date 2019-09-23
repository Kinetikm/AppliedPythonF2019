#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    size = len(list_of_lists)
    det = 1
    num_trans = 0
    for i in range(size):
        if len(list_of_lists[i]) != size:
            return None
    for i in range(size):
        pusher = i
        for j in range(i + 1, size):
            if abs(list_of_lists[j][i]) > abs(list_of_lists[pusher][i]):
                pusher = j
        list_of_lists[i], list_of_lists[pusher] = list_of_lists[pusher], list_of_lists[i]
        if i != pusher:
            num_trans += 1
        det *= list_of_lists[i][i]
        for j in range(i + 1, size):
            list_of_lists[i][j] /= list_of_lists[i][i]
        for j in range(size):
            if j != i:
                for k in range(i + 1, size):
                    list_of_lists[j][k] -= list_of_lists[i][k] * list_of_lists[j][i]
    return det * (-1)**num_trans
