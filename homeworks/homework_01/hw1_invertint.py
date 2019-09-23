#!/usr/bin/env python
# coding: utf-8


def reverse(number):
    '''
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
	'''
    sign = 1
    if number == 0:
    	return 0
    num = str(number)
    if num[0] == '-':
        sign = -1
        num = num[1:]
    num = num[::-1]
    while num[0] == '0':
        num = num[1:]
    return sign * int(num)
    raise NotImplementedError
