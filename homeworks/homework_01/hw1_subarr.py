#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    diff = dict()
    last_sum = 0
    for i, val in enumerate(input_lst):
        last_sum += val
        if last_sum == num:
            return 0, i
        if val == num:
            return i, i

        if last_sum - num in diff:
            return diff[last_sum - num], i
        diff[last_sum] = i + 1
    return ()
