#!/usr/bin/env python
# coding: utf-8


def check(mas):
    tmp = len(mas)
    for x in mas:
        if len(x) != tmp:
            return None
    return tmp


def deter(tens):
    if len(tens) == 1:
        return tens[0][0]
    if len(tens) == 2:
        return tens[0][0] * tens[1][1] - tens[1][0] * tens[0][1]
    tm = -1
    for i in range(len(tens)):
        if tens[0][i] != 0:
            tm = i
            break
    if tm == -1:
        return 0
    det = tens[0][tm]
    for i in range(1, len(tens)):
        if i == tm:
            continue
        x = tens[0][i]/tens[0][tm]
        for j in range(len(tens)):
            tens[j][i] -= x*tens[j][tm]
    exp = -1 if tm % 2 != 0 else 1
    b = tens[1:]
    b = [[b[g][k] for k in range(len(b[g])) if k != tm] for g in range(len(b))]
    return exp*det*deter(b)


def calculate_determinant(list_of_lists):
    tmp = check(list_of_lists)
    if tmp is None:
        return None
    return deter(list_of_lists)
