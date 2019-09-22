#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    
    dct = {}
    sum = 0
    for el, i in zip(input_lst, range(len(input_lst))):
        sum += el
        if sum == num:
            return 0, i
        if el == num:
            return i, i
        if sum - num in dct:
            return dct[sum-num] + 1, i
        dct[sum] = i
    return ()
