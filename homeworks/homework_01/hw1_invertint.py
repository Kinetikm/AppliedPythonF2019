#!/usr/bin/env python
# coding: utf-8


def reverse(num):
    sign = 1
    if num < 0:
        sign = - 1
    list1 = list(str(abs(num)))
    list1.reverse()
    str1 = "".join(list1)
    num1 = int(str1)
    return sign*num1
