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
    hash_map = {}
    for i, val in enumerate(input_list):
        if (target - val) in hash_map:
            return (hash_map[target - val], i)
        hash_map[val] = i
    return None
