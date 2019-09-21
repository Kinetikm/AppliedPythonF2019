#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    """
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    """
    k = 1
    if number < 0:
        k = -1
    return k * int(str(abs(number))[::-1])