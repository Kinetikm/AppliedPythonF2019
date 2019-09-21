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

    sum_dict = {}
    tmp_sum = 0
    for i, val in enumerate(input_lst):
        tmp_sum += val
        if tmp_sum - num in sum_dict:
            ret = (sum_dict[tmp_sum - num], i)
            return ret
        elif val == num:
            ret = (i, i)
            return ret
        else:
            sum_dict[tmp_sum - val] = i
    return tuple()
