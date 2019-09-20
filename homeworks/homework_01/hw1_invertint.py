#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    flag = 0
    if number < 0:
        flag = 1
        number *= -1
    res = 0
    while number > 0:
        res = res * 10 + number % 10
        number = number // 10
    return res if flag == 0 else -res
