#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    def reverse(number):
    b = 0
    while number > 0:
        b = b * 10 + number % 10
        number //= 10
    return b
    raise NotImplementedError
