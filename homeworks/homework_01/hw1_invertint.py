#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    s = number
    number = str(abs(number))
    number = number[::-1]
    if s < 0:
        return -int(number)
    else:
        return int(number)
