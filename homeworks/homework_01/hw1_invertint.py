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
if number > 0:
    while number > 0:
        b = b * 10 + number % 10
        a = a // 10
else:
    number = number*(-1)
    while a > 0:
        b = b * 10 + a % 10
        number = number // 10
    b = b* (-1)
print(b)
raise NotImplementedError
