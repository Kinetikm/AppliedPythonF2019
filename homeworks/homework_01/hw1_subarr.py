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

    for iterator in range(len(input_lst)):
        summ = 0
        for sec_iterator in range(iterator, len(input_lst)-1):
            summ = summ + input_lst[sec_iterator]
            if summ == num:
                vivod = (iterator,sec_iterator)
                return vivod
    else:
        return ()