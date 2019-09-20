#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    nnumber = 0
    while number != 0:
        nnumber = nnumber * 10 + (number % 10)
        number = number // 10
    return nnumber
