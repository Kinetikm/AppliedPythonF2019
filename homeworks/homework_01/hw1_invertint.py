#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    new_number = 0
    if number >= 0:
        while number > 0:
            res = number % 10
            number = number // 10
            new_number = 10 * new_number
            new_number = new_number + res
    else:
        number_ = number * (-1)
        while number_ > 0:
            res = number_ % 10
            number_ = number_ // 10
            new_number = 10 * new_number
            new_number = new_number + res
        new_number = new_number * (-1)
    return new_number
