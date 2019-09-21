#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    sign = 1 if number >= 0 else -1
    number *= sign
    res = 0
    while number != 0:
        res = res * 10 + number % 10
        number = number // 10
    return sign * res
