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
    lastSum = 0
    d = dict()
    for i in range(len(input_lst)):
        lastSum = lastSum+input_lst[i]
        if lastSum == num:
            return (0, i)
        elif (lastSum-num) in d:
            return (d.get(lastSum-num)+1, i)
        d[lastSum] = i
    return tuple()
    raise NotImplementedError
