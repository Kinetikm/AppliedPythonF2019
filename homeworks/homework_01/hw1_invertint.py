#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    flar = 0
    if number < 0:
        flag = 1
    b_b = abs(number)
    b = str(b_b)
    c = b[::-1]
    d = int(c)
    if flag == 1:
        d *= -1
    return d
