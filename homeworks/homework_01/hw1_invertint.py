#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    a = number
    sign = 1
    if a < 0:
        sign = -1
        a = -a
    b = str(a)
    b = b[::-1]
    b = int(b) * sign
    return b
