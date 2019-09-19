#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    i = abs(number)
    vixod = 0
    while i > 0:
        vixod = vixod * 10 + (i % 10)
        i = i // 10
    if number >= 0:
        return vixod
    else:
        return -vixod