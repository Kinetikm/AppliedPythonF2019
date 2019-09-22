#!/usr/bin/env python
# coding: utf-8
def find_subarr(input_lst, num):
    dict = {}
    sum = 0
    for idx, val in enumerate(input_lst):
        sum += val
        if sum - num in dict:
            return (dict[sum-num], idx)
        elif val == num:
            return (idx, idx)
        else:
            dict[sum - val] = idx
    return ()
    raise NotImplementedError
