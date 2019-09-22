#!/usr/bin/env python
# coding: utf-8


def find_indices(input_list, target):
    '''
    Метод возвращает индексы двух различных
    элементов listа, таких, что сумма этих элементов равна
    n. В случае, если таких элементов в массиве нет,
    то возвращается None
    Ограничение по времени O(n)
    :param input_list: список произвольной длины целых чисел
    :param target: целевая сумма
    :return: tuple из двух индексов или None
    '''
    sols_dict = dict()
    for i, val in enumerate(input_list):
        if val in sols_dict:
            return [sols_dict[val], i]
        else:
            if (target - val) not in sols_dict:
                sols_dict[target - val] = i
    return None
