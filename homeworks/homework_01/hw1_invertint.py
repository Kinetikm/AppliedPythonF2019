#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    sgn = 1
    if number < 0:
        sgn = -1
    number = int(str(abs(number))[::-1])*sgn
    return number
