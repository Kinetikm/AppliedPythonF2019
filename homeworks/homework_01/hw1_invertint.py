#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    number_2 = 0
    while number != 0:
        number_2 = number_2 * 10
        number_2 += number % 10
        number = number // 10
        
    return number_2

l = reverse(123456789)
