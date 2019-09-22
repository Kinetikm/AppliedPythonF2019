#!/usr/bin/env python
# coding: utf-8


def check_palindrom(digit):
    for i in range(len(digit)):
        if digit[i] != digit[-1 - i]:
            return False
    return True
