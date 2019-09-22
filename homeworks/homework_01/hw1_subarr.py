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
    if len(input_lst) == 0:
        return ()
    s = input_lst[0]
    l = 0
    r = 0
    while (l < len(input_lst)) and (r < len(input_lst)):
        if s < num:
            if r + 1 < len(input_lst):
                r += 1
                s += input_lst[r]
            else:
                return ()
        elif s > num:
            s -= input_lst[l]
            l += 1
        else:
            return (l, r)
    return ()
