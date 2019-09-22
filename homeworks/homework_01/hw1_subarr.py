#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    summ = dict()
    temp = 0
    for i, j in enumerate(input_lst):
        temp += j
        if temp == num:
            return 0, i
        elif j == num:
            return i, i
        if (temp - num) in summ:
            return summ[temp - num], i
        summ[temp] = i + 1
    return ()
