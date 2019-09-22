#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    tmp = {}
    sum = 0
    for indx, zn in enumerate(input_lst):
        sum += zn
        if sum - num in dict:
            return(dict[sum - num], indx)
        elif zn == num:
            return(indx, indx)
        else:
            dict[sum - val] = indx
    return()
