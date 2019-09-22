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
    sub_sums = dict()
    sub_sum = 0
    for i, val in enumerate(input_lst):
        sub_sum += val
        if sub_sum == num:
            return 0, i
        elif sub_sum - num not in sub_sums:
            sub_sums[sub_sum] = i
        else:
            return sub_sums[sub_sum - num] + 1, i
    return ()

