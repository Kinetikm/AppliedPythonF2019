#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    a = {}
    sum = 0
    for i, value in enumerate(input_lst):
        sum += value
        if sum - num in a:
            return(a[sum - num], i)
        elif value == num:
            return(i, i)
        else:
            a[sum - value] = i
    return()
    '''
    Метод, находящий подмассив, сумма чисел которого равна заданному числу
    O(n) по времени
    :param input_lst: массив
    :param num: искомое число
    :return: два индекса (начала и конца подмассива). Пустой tuple, если таких нет
    Пример: find_subarr([1, 2, 3, 4, 5, -1], 4) может вернуть (3, 3) или (4, 5)
    '''
