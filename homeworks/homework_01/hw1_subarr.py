#!/usr/bin/env python
# coding: utf-8


def find_subarr(a, s):
    index1 = 0
    index2 = 0
    while index1 + index2 < 2*len(a) - 2:
        midsum = a[index1] + a[index2]
        if midsum != s:
            if index1 >= index2:
                index2 += 1
            else:
                index1 += 1
        else:
            return index1, index2
    return ()
# метод нахождения подмассива с заданной суммой
