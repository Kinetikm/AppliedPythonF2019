#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''

    flag = 0
    if number < 0:
        number = abs(number)
        flag = 1
    array = str(number)
    length = len(array)
    i = 0
    sum = 0

    if length == 1:
        return number
    while i < length // 2:
        sum += (int(array[-1-i]) * (10**(length-i-1))) + (int(array[i]) * (10**i))
        i += 1
    if length % 2 != 0:
        sum += int(array[length // 2]) * 10**(length // 2)

    if flag:
        return -sum
    return sum
    # raise NotImplementedError
