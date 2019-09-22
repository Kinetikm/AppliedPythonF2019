#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    sum = 0
    hash = {}
    for index, value in enumerate(input_lst):
        sum += value
        if sum - num in hash:
            return (hash[sum - num], index)
        elif value == num:
            return (index, index)
        else:
            hash[sum - value] = index
    return ()
