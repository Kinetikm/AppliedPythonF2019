#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    i = 1
    j = i - 1
    while j < len(input_lst):
        while i <= len(input_lst):
            if sum(input_lst[j:i]) == num:
                print(j, i - 1)
            i +=1
        i = j + 2
        j += 1
    '''
    Метод, находящий подмассив, сумма чисел которого равна заданному числу
    O(n) по времени
    :param input_lst: массив
    :param num: искомое число
    :return: два индекса (начала и конца подмассива). Пустой tuple, если таких нет
    Пример: find_subarr([1, 2, 3, 4, 5, -1], 4) может вернуть (3, 3) или (4, 5)
    '''
    raise NotImplementedError
