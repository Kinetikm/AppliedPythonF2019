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
    for i in range(len(input_lst)):
        d[i] = sum(input_lst[i::])
        if d[i] == num:
            return (i, len(input_lst) - 1)
    for r in range(len(input_lst)):
        l = 0
        while l < r:
            if d[l] - d[r] == num:
                return (l, r - 1)
            l += 1
    return ()
