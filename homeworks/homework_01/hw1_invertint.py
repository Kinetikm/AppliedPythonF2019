#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    print(number)
    absnumber = abs(number)
    res = 0
    while absnumber >= 10:
        print(absnumber)
        res *= 10
        res += absnumber % 10
        absnumber //= 10
    res *= 10
    res += absnumber
    if number < 0:
        res *= (-1)
    return res
