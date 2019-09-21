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
    Пример: find_subarr([1, 2, 3, 4, 5, -1], 4) может вернуть (3, 3)
    или (4, 5)
    '''
    sum_dict = {}
    cur_sum = 0

    for i in range(len(input_lst)):
        cur_sum += input_lst[i]
        if cur_sum == num:
            return (0, i)
        sum_dict[cur_sum] = i
        if (cur_sum - num) in sum_dict:
            return (sum_dict[cur_sum - num] + 1, i)

    return ()
