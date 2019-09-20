#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    n_number = 0
    while number != 0:
        n_number = n_number * 10 + (number % 10)
        number = number // 10
    return n_number
