#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    '''
    Метод, находящий подмассив, сумма чисел которого равна заданному числу
    O(n) по времени
    :param input_lst: массив
    :param num: искомое число
    :return: два индекса (начала и конца подмассива).
    Пустой tuple, если таких нет
    Пример: find_subarr([1, 2, 3, 4, 5, -1], 4) ]
    может вернуть (3, 3) или (4, 5)
    '''
    myDict = dict()
    prev = 0
    summ = sum(input_lst)
    myDict[summ] = 0
    if num == summ:
        return 0, len(input_lst) - 1
    for i, val in enumerate(input_lst):
        if val == num:
            return (i, i)
        if prev == num:
            return 0, i - 1
        if summ - prev - val + num in myDict:
            return (myDict[summ - prev - val + num], i)
        else:
            if summ - prev - val not in myDict:
                myDict[summ - prev - val] = i + 1
            prev += val
    return ()
