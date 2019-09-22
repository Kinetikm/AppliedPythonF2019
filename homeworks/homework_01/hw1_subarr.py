#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    d = {}
    summ = 0
    for i, value in enumerate(input_lst):
        summ += value
        if summ - num in d:
            return (d[summ - num], i)
        elif value == num:
            return (i, i)
        else:
            d[sum - value] = i
    return()
