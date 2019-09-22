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
    sums = dict()
    curr_sum = 0
    for (i, el) in enumerate(input_lst):
        curr_sum += el
        if curr_sum == num:
            return (0, i)

        delta = curr_sum - num
        if delta in sums:
            return (sums[delta]+1, i)

        sums[curr_sum] = i

    return ()

