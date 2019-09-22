#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    k = 0
    if number > 0:
        while number > 0:
            k = k*10+number % 10
            number //= 10
        return k
    else:
        a = a * (-1)
        while number > 0:
            k = k * 10 + number % 10
            number //= 10
        return -k
    return k
