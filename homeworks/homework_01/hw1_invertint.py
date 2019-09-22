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
    if num < 0:
        num *= -1
        while num != 0:
            new *= 10
            new += num % 10
            num = num // 10
        new *= -1
    else:
        while num != 0:
            new *= 10
            new += num % 10
            num = num // 10
    return new
