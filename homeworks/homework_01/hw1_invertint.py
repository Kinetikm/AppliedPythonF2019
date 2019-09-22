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
        number *= -1
        sign = 0
    number = abs(number)
    number = str(number)
    number = number[::-1]
    number = int(number)
    if sign == 0:
        number *= -1
    return number
