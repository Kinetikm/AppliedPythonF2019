#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    number = str(number)
    if number[0] == '-':
        number = -(int(number[:0:-1]))
    else:
        number = int(number[::-1])
    return number
