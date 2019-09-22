#!/usr/bin/env python
# coding: utf-8


def check_palindrom(A):
    '''
    Метод проверяющий строку на то, является ли
    она палиндромом.
    :param A: строка
    :return: True, если строка являестя палиндромом
    False иначе
    '''
    A = ''.join(A.lower().split())
    B = A[::-1]
    return True if B == A else False
