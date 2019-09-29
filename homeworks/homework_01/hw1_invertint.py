#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    chek = 1
    if number < 0:
        chek = -1
    b = str(abs(number))
    b = b[::-1]
    number = int(b) * chek
    return number