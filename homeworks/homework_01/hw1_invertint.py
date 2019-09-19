#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    if number < 0:
        is_negativ_flag = True
    else:
        is_negativ_flag = False
    reverse = 0
    number = abs(number)
    while (number > 0):
        reminder = number % 10
        reverse = (reverse * 10) + reminder
        number = number // 10
    if is_negativ_flag:
        reverse *= -1
    return reverse