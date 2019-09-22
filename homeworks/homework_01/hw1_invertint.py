#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    if number < 0:
        return -1*int(str(-1*number)[::-1])
    return int(str(number)[::-1])
