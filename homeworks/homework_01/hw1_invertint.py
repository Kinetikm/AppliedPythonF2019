#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    if number < 0:
        k = -1
    else:
        k = 1
    number = abs(number)
    nout = 0
    while abs(number) > 0:
        l = number % 10
        number = number // 10
        nout = nout * 10 + l
    return k * nout
