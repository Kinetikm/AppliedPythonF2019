#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    
    k = 1
    n = 0
    r = 0
    if number < 0:
        number = -number
        k = -1
    while number >= 1:
        #k = k * 10
        n = number % 10
        number = number // 10
        r = r * 10 + n
    r = r * k
    return r
    raise NotImplementedError
