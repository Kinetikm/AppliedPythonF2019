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
	for i in range(0, len(input_lst) - 2):
		 if input_lst[i] == num:
		    return (i,i)
		 if ((input_lst[i] + input_lst[i+1]) == num):
		    return (i,i+1)
	    return ()
    raise NotImplementedError
