#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    '''
    Метод, находящий подмассив,
    сумма чисел которого равна заданному
    числу
    O(n) по времени
    :param input_lst: массив
    :param num: искомое число
    :return: два индекса (начала и конца подмассива).
    Пустой tuple, если таких нет
    Пример: find_subarr([*1,1,1, 4*, 2, 3, 4, 5, -1], 4)
    может вернуть (3, 3) или (4, 5)
    '''
    mydict = dict()
    summa = 0
    for i in range(len(input_lst)):
        mydict[summa] = i
        if summa - num in mydict:
            return (mydict[summa - num], i-1)
        summa += input_lst[i]
    if summa - num in mydict:
        return (mydict[summa - num], len(input_lst)-1)
    return ()
