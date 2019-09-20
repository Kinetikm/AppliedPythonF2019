#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    fl = 1
    if number < 0:
        fl = -1
        number = number * fl
    n_number = 0
    while number != 0:
        n_number = n_number * 10 + (number % 10)
        number = number // 10
    return fl * n_number
