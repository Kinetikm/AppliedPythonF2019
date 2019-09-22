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
    if (len(input_lst) == 0):
        return ()
    t = input_lst[0]
    for i in range(1, len(input_lst)):
        if (num == input_lst[i]):
            return (i, i)
        elif (num == t + input_lst[i]):
            return (i-1, i)
        t = input_lst[i]
    return ()