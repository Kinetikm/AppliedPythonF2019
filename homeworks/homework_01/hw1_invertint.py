#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    if number < 0:
        number *= -1
        number = str(number)
        number = number[::-1]
        number = int(number)
        number *= -1
    else:
        number = str(number)
        number = number[::-1]
        number = int(number)
    return number
