#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    if number >= 0:
        return int(str(number)[::-1])
    else:
        return int(str(number * - 1)[::-1]) * - 1
