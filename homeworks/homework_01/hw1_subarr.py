#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    l = len(input_lst)
    start = 0
    end = 0
    sum = input_lst[0]
    while (start < l) and (end < l):
        if sum == num:
            return (start, end)
        if end < l - 1:
            sum += input_lst[end]
            end += 1
        elif end == l - 1:
            start += 1
            sum = input_lst[start]
            end = start
    return ()
