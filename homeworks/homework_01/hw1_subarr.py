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
    
    n = 0
    k = 0
    d = dict()
    j = 0
    for i, val in enumerate(input_lst):
        #print("la-la")
        if val == num:
            return (i, i)
        if (num - val) in d:
            return (d[num - val][1], i)
        #j = 0
        #d[val] = [k + val, i]
        v = k
        #print("val = {0}".format(val))
        for l in range(0, j, 1):
            #print(k)
            d[k + val] = d[k]
            h = k
            k = d[k + val][0]
            d[h + val][0] = d[h + val][0] + val
            d.pop(h)
        #d[k + val] = d[k]
        d[val] = [v + val, i]
        
        k = val
        #n = n + val
        j = j + 1
    
    return tuple()
    
    raise NotImplementedError
