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
    if number != 0:
        sign = number // abs(number)
    number = abs(number)
    return int(str(number)[::-1])*sign
