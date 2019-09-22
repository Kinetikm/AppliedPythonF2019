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
    s = 0
    for i in range(len(input_lst)):
		if input_lst[i] > num:
			s = 0
			continue
		if input_lst[i] == num:
			return (i, i)
		s = input_lst[i]
		for j in range(i + 1, len(input_lst)):
			if input_lst[j] > num:
				s = 0
				break
			if input_lst[j] == num:
				return (j, j)
			else:
				s = s + input_lst[j]
			if s == num:
				return (i, j)
		s = 0
    return ()