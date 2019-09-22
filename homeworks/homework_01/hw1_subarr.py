#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    tmp = {}
    summary = 0
    for indx, zn in enumerate(input_lst):
        summary += zn
        if summary - num in tmp:
            return(tmp[summary - num], indx)
        elif zn == num:
            return(indx, indx)
        else:
            tmp[summary - zn] = indx
    return()
