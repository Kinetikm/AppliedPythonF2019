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
    sum_ = 0
    temp_dict = {}
    for i, item in enumerate(input_lst):
        sum_ += item
        if sum_ == num:
            return (0, i)
        if sum_ - num in temp_dict:
            return (temp_dict[sum_ - num] + 1, i)
        temp_dict[sum_] = i
    return ()
