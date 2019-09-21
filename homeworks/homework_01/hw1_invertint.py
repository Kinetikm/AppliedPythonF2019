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
        s = '-'
        number = -1 * number
    else:
        s = ''
    string, new_string = str(number), []
    for i in range(len(string)):
        new_string.append(string[i])
    while True:
        if new_string[-1] == '0' and len(new_string) != 1:
            new_string.pop()
        else:
            break
    new_string = new_string[::-1]
    for i in range(len(new_string)):
        s += new_string[i]
    return int(s)
