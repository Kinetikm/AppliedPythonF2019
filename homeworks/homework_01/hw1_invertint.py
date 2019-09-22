#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    prm = False
    if number < 0:
        prm = True
        number *= -1
    number = str(number)
    number = number[::-1]
    number = int(number)
    if prm:
        number *= -1
    return number
