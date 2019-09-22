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
    d = {0: -1}
    s = 0
    r = 0
    while r < len(input_lst):
        s += input_lst[r]
        if d.get(s - num) is not None:
            print(s)
            return(d.get(s - num) + 1, r)
        d[s] = r
        r += 1
    return ()
