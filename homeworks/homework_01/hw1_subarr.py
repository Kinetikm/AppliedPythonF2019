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
    cnt = 0
    for i in range(0, len(input_lst)):
        list_sums = list(sums(input_lst[i:]))
        if num in list_sums:
            return tuple([i, list_sums.index(num)+i])
    if cnt == 0:
        return tuple()


def sums(lst):
    total = 0
    for el in lst:
        total += el
        yield total


if __name__ == '__main__':
    print(find_subarr([1, 2, 3, 4, 5, -1], 23))
