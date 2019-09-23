#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    s = input_lst
    n = num
    if len(s) == 0:
        return s
    blank = ()
    sum = 0
    d = {}
    for i in range(len(s)):
        sum += s[i]
        if sum == n:
            return (0, i)
        if sum - num in d:
            return (d[sum-n] + 1, i)
        d[sum] = i
    return blank
