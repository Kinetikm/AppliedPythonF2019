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
    input_dict = {}
    answer = 0
    for num, el in enumerate(input_list):
        input_dict[el] = num
    for key in input_dict:
        num = target - key
        if input_dict.get(num, 'num is absent') != 'num is absent' and \
                input_dict[key] != input_dict[num]:
            answer = 1
            return tuple([input_dict[key], input_dict[num]])
        else:
            continue
    if answer == 0:
        return None
