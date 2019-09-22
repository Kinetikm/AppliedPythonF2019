#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    result = 0
    sign = 1
    if number < 0:
        sign = -1
        number *= -1
    while number > 0:
        result = result * 10 + number % 10
        number = number // 10
    result *= sign
    return result
