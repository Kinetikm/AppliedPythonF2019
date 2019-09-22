#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    res = 0
    flag = False
    if number < 0:
        flag = True
        number = abs(number)
    while number > 0:
        temp = number % 10
        res = (res * 10) + temp
        number = number // 10
    if flag:
        return -res
    else:
        return res
