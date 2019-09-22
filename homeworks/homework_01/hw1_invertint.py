#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''

    # print(number)

    if number == 0:
        return 0

    num_sign = abs(number) / number

    res = 0
    number = abs(number)
    while(number > 0):
        mod = number % 10
        if res != 0 or mod != 0:
            res *= 10
            res += mod

        number //= 10

    return int(num_sign * res)

