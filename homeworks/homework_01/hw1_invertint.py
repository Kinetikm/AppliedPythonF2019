#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    return -int(str(abs(number))[::-1]) if number < 0 \
            else int(str(abs(number))[::-1])
