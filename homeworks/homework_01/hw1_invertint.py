#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    raise NotImplementedError
    c = 0
    a_ = abs(number)
    while a_ > 0:
        b = a_ % 10
        a_ = a_ // 10
        c = b + c * 10
    if number > 0:
        return c
    else:
        return -1 * c
