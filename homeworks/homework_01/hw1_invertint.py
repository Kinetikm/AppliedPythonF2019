#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    if (number < 0):
        flag = 1
        number = number * (-1)
    else:
        flag = 0
    c = str(number)
    d = ''.join(reversed(c))
    if (flag > 0):
        number = int(d) * (-1)
    else:
        number = int(d)
    return number
    raise NotImplementedError
