#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    '''
    Метод, находящий подмассив, сумма чисел которого равна заданному числу
    O(n) по времени
    :param input_lst: массив
    :param num: искомое число
    :return: два индекса (начала и конца подмассива). Пустой tuple, если таких нет
    Пример: find_subarr([1, 2, 3, 4, 5, -1], 4) может вернуть (3, 3) или (4, 5)
    '''
    d = {}
    s = 0
    for i in range(len(input_lst)):
        s += input_lst[i]
        if s == num:
            return 0, i
        if s - num in d:
            return d[s - num] + 1, i
        d[s] = i
    return tuple()
