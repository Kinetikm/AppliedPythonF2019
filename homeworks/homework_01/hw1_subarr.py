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
    d = dict()
    i = 0
    result = 0
    while i < len(input_lst):
        result += input_lst[i]
        if result == num:
            return (0, i)
        if result - num in d:
            return (d[result - num] + 1, i)
        d[result] = i
        i += 1
    return ()
