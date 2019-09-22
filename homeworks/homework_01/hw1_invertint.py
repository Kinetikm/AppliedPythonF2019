#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    if number > 0:
        sign = 1
    else:
        sign = -1
    number = abs(number)
    rev_int = number % 10
    number = number // 10
    while number > 9:
        rev_int = rev_int * 10 + (number % 10)
        number = number // 10
    rev_int = rev_int * 10 + number
    rev_int *= sign
    return rev_int
