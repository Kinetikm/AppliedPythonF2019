#!/usr/bin/env python
# coding: utf-8


def reverse(num):
    sign = int(num/abs(num))
    list1 = list(str(abs(num)))
    list1.reverse()
    str1 = "".join(list1)
    num1 = int(str1)
    return sign*num1
