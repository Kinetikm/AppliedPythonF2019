#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    sign = number // abs(number)
    inverted = 0
    number = abs(number)
    while number > 0:
        inverted *= 10
        inverted += (number % 10)
        number //= 10
    return sign*inverted
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''