#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    mas = []
    sum = 0
    for i in range(len(input_lst)):
        a = input_lst[i]
        if a == num:
            return (i, i)
        sum += a
        if  sum - num not in mas:
            mas.append(sum - num)
        else:
            return (mas.index(sum - num), i)
    return ()

