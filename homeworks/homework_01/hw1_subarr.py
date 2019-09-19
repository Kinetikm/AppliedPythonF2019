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
    summa = 0
    dic = dict()
    for count, val in enumerate(input_lst):
        summa += val
        dic[summa] = count
        if (summa - num) in dic:
            return (dic[summa - num] + 1, count)
        elif summa == num:
            return (0, count)

    return ()
