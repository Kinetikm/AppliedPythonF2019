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
    sols_dict = dict()
    sols_dict[0] = -1  # Если массив состоит из одного элемента
    temp_sum = 0
    for i, val in enumerate(input_lst):
        temp_sum += val
        if temp_sum - num in sols_dict:
            return sols_dict[temp_sum - num] + 1, i
        else:
            sols_dict[temp_sum] = i
    return ()
