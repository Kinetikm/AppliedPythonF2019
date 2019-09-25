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
    # summ = 0
    # tup = ()
    # for i in range(len(input_lst)):
    #     for k in range(i, len(input_lst)):
    #         summ += input_lst[k]
    #         if summ == num:
    #             tup = (i, k)
    #             return tup
    #     summ = 0
    # return tup

    sum, table = 0, {}

    for i, value in enumerate(input_lst):
        print(i, value, sum, end = ' ')
        print(table)
        sum += value
        if sum == num:
            return (0, i)
        if sum - num in table:
            return (table[sum - num] + 1, i)
        else:
            table[sum] = i

    return ()

print(find_subarr([1, 2, 3, 4, 5, -1], 5))