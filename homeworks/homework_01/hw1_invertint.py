#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    x = abs(number)
    res = x % 10
    x = x//10
    while x != 0:
        res = res*10+x % 10
        x = x//10
    if number < 0:
        return -res
    else:
        return res
    raise NotImplementedError
