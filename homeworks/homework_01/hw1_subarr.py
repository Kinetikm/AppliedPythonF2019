#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    """
    Метод, находящий подмассив, сумма чисел которого равна заданному числу
    O(n) по времени
    :param input_lst: массив
    :param num: искомое число
    :return: два индекса (начала и конца подмассива). Пустой tuple, если таких нет
    Пример: find_subarr([1, 2, 3, 4, 5, -1], 4) может вернуть (3, 3) или (4, 5)
    """
    dict_of_sum = {}
    part_sum = 0
    for i in range(len(input_lst)):
        part_sum = part_sum + input_lst[i]
        if part_sum == num:
            return (0, i)
        elif part_sum - num in dict_of_sum:
            return (dict_of_sum[part_sum - num]+1, i)
        dict_of_sum[part_sum] = i
    return ()
