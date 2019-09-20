#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    b = 0
    flag = False
    if number < 0:
        flag = True
        number *= -1
    while number > 0:
        b = b * 10 + number % 10
        number //= 10
    if flag:
        b *= -1
    return b
