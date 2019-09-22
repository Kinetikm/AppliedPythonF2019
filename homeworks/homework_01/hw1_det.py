#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    def perestanovki(elements):
        if len(elements) <= 1:
            yield elements
        else:
            for perm in perestanovki(elements[1:]):
                for i in range(len(elements)):
                    yield perm[:i] + elements[0:1] + perm[i:]

    if len(list_of_lists) < 1 or len(list_of_lists[0]) < 1:
        return None
    for it in list_of_lists:
        if len(it) != len(list_of_lists):
            return None
    fact = 1
    origin = []
    for k in range(len(list_of_lists)):
        fact *= (k + 1)
        origin.append(k)
    total = 0
    for mas in perestanovki(origin):
        same = 1.0
        counter = 0
        tmp = mas.copy()
        while tmp != origin:
            for i, j in enumerate(tmp):
                if j != origin[i]:
                    tmp[i], tmp[j] = tmp[j], tmp[i]
                    counter += 1
        for j in range(len(list_of_lists)):
            if mas[j] == origin[j]:
                same *= list_of_lists[mas[j]][mas[j]]
            elif mas[j] != origin[j]:
                same *= list_of_lists[origin[j]][mas[j]]
        total += ((-1) ** counter) * same
    return total
