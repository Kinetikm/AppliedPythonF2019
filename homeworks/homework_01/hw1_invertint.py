#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    sign = 1
    if number < 0:
        sign = -1
        number *= sign
    return int(str(number)[::-1]) * sign
