#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''

    new = 0
    if number < 0:
        number *= -1
        while number != 0:
            new *= 10
            new += number % 10
            number = number // 10
        new *= -1
    else:
        while number != 0:
            new *= 10
            new += number % 10
            number = number // 10
    return new
