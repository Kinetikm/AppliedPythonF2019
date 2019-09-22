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
    res_contain = []
    
    for index in range(1, len(input_list)):
        if input_list[index - 1] == num:
            res_contain.append([index - 1, index - 1])
        
        if input_list[index - 1] + input_list[index] == num:
            res_contain.append([index - 1, index])

    res = (res_contain[0][0], res_contain[0][1])

    return res
