#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    import copy
    for l in list_of_lists:
        if len(l) != len(list_of_lists):
            return None

    def cut_matrix(Matr, k):
        if len(Matr) == 1:
            return Matr
        else:
            M = copy.deepcopy(Matr)
            M[0: 1] = []
            for s in M:
                s[k:k + 1] = []
        return M

    if len(list_of_lists) == 1:
        return list_of_lists[0][0]
    else:
        det = 0
        for j in range(len(list_of_lists)):
            det += ((-1) ** j) * list_of_lists[0][j] * \
                   calculate_determinant(cut_matrix(list_of_lists, j))
        return det
