#!/usr/bin/env python
# coding: utf-8


def find_subarr(a, num):
    a_dict = {}
    sum = 0
    for i in range(len(a)):
        sum += a[i]
        if (sum == num):
            return(0, i)
        if (sum - num) in a_dict:
            return(a_dict[sum - num] + 1, i)
        else:
            a_dict[sum] = i
    return()
