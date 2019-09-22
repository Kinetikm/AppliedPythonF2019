#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    chek = 1
    if number < 0:
        check = -1
    b_b = abs(number)
    b = str(b_b)
    c = ''.join(reversed(b))
    print(c)
    d = int(chek) * int(c)
    return d
