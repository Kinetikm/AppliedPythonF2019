#!/usr/bin/env python
# coding: utf-8
import itertools

def find_subarr(s, num):
    '''
    Метод, находящий подмассив, сумма чисел которого равна заданному числу
    O(n) по времени
    :param s: массив
    :param num: искомое число
    :return: два индекса (начала и конца подмассива). Пустой tuple, если таких нет
    Пример: find_subarr([1, 2, 3, 4, 5, -1], 4) может вернуть (3, 3) или (4, 5)
    '''
    N = len(s)+1
    x = i = j = 0
    while x < N:
        j += x
        while i < N and j < N:
            if num == sum(s[i:j+1]):
                return (i,j)
            i += 1
            j += 1
        i, j = 0, 0
        x += 1
    return tuple()

