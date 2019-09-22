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
    if (number < 0):
        number *= -1
        k = -1
    a = []
    new_number = 0
    while(number > 0):
        a.append(number % 10)
        number //= 10
    a = a[::-1]
    for i in range(len(a)):
        new_number += a[i]*10**i
    new_number *= k
    return new_number
