#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    chek = number/abs(number)
    b_b = abs(number)
    b = str(b_b)
    c = ''.join(reversed(b))
    print(c)
    d = int(chek) * int(c)
    return d
