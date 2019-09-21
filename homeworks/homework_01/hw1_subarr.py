#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    t = a[0]
    for i in range(1,len(a)):
        if (num == a[i]):
            return (i,i)
        elif (num == t + a[i]):
            return (i-1,i)
        t = a[i]
    raise NotImplementedError
