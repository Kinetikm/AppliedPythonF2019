#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    dictionary = {}
    sum = 0
    for i in range(len(input_lst)):
        sum += input_lst[i]
        if sum == num:
            return 0, i
        if sum - num in dictionary:
            return dictionary[sum - num] + 1, i
        dictionary[sum] = i
    return ()
