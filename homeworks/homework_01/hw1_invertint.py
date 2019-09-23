#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    flag_on_minus = False
    if number < 0:
        number *= -1
        flag_on_minus = True
    number = int(str(number)[::-1])
    if flag_on_minus:
        number *= -1
    return number
