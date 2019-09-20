#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    '''
    answ = ''
    divider = 1
    negative = False
    if number < 0:
        number *= -1
        negative = True
    for i in range(len(str(number))):
        temp_digit = (number % (divider * 10)) // divider
        answ += str(temp_digit)
        divider *= 10
    if negative:
        return -int(answ)
    return int(answ)
    '''
    Можно сделать проще путём приведения к строке и взятием среза [::-1],
    но оставил способ с получением тдельных цифр, т к он интереснее
    '''
