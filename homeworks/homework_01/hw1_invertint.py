#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    if (number // 10) == 0:
        print(0)
    while number > 0:
        if number % 10 > 0:
            print(number % 10, end='')
        number = number // 10
    raise NotImplementedError
