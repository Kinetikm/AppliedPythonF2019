#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    b = 0
    f = 0
    if number < 0:
        f = 1
        number = abs(number)
    while (number > 0):
        b *= 10
        b += (number % 10)
        number //= 10
    if f:
        b = -b
    return b
