#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    if number == 0:
        return 0
    else:
        while number % 10 == 0:
            number /= 10
        k = int(number / abs(number))
        a = str(int(abs(number)))
        a = a[::-1]
        number = int(a)
        return k * number
