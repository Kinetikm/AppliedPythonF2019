#!/usr/bin/env python
# coding: utf-8


def reverse(number):

    if number < 0:
        string = str(-number)[::-1]
        return -int(string)
    else:
        string = str(number)[::-1]
        return int(string)
