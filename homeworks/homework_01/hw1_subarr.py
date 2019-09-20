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
    if len(input_lst) == 0:
        return ()

    part_sums = [input_lst[0]]
    d = {}

    # find partial sums: sum[i] = lst[0] + .. +lst[i]
    for i in range(1, len(input_lst)):
        next_part_sum = part_sums[i - 1] + input_lst[i]
        part_sums.append(next_part_sum)

    # sums[j] - sum[i] = num. fills map with sums[j] - num = sum[i]
    for j in range(len(part_sums)):
        d[part_sums[j] - num] = j

    # if num is already in part_sums(-> [0:j])
    if num in part_sums:
        return 0, part_sums.index(num)

    ans = ()
    for i, el in enumerate(part_sums):
        if el in d:
            # sums[j] - sums[i] = num, j >= i
            j = d[el]
            if j >= i:
                ans = i + 1, j
                return tuple(ans)

    return ()
