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
    dict = {}

    summa = 0

    for idx, val in enumerate(input_lst):
        summa += val
        if summa - num in dict:
            return(dict[summa - num], idx)
        elif val == num:
            return (idx, idx)
        else:
            dict[summa - val] = idx

    return ()
