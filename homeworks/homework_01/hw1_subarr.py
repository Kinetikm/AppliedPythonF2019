#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    mas = [0]
    sum = 0
    for i in range(len(input_lst)):
        a = input_lst[i]
        if a == num:
            return (i, i)
        sum += a
        if sum - num not in mas:
            mas.append(sum)
        else:
            return (mas.index(sum - num), i)
    return ()
