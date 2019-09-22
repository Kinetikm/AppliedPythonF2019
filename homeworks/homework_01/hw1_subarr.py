#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    '''
    Метод, находящий подмассив, сумма чисел которого равна заданному числу
    O(n) по времени
    :param input_lst: массив
    :param num: искомое число
    :return: два индекса (начала и конца подмассива). Пустой tuple,
        если таких нет
    Пример: find_subarr([1, 2, 3, 4, 5, -1], 4) может вернуть (3, 3) или (4, 5)
    '''

    d = dict()
    _sum = 0
    for ind, val in enumerate(input_lst):
        _sum += val
        if _sum == num:
            return (0, ind)
        if val == num:
            return (ind, ind)
        if (_sum - num) in d:
            return (d[_sum - num], ind)
        d[_sum] = ind + 1
    return ()
