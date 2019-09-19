#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    number = str(number)
    if number[0] == '-':
        number = list(number[1:])
        number.reverse()
        number = -(int("".join(number)))
    else:
        number = list(number)
        number.reverse()
        number = int("".join(number))
    return number
