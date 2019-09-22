import copy


def minor(matrix, i, j):
    M = copy.deepcopy(matrix)
    del M[i]
    for i in range(len(matrix[0]) - 1):
        del M[i][j]
    return M


import copy


def minor(matrix, i, j):
    M = copy.deepcopy(matrix)
    del M[i]
    for i in range(len(matrix[0]) - 1):
        del M[i][j]
    return M


def calculate_determinant(list_of_lists):
    n = len(list_of_lists)
    for i in range(n):
        if n != len(list_of_lists[i]):
            return None
    if n == 1:
        return list_of_lists[0][0]
    sign = 1
    det = 0
    for j in range(n):
        det += list_of_lists[0][j] * sign * calculate_determinant(minor(list_of_lists, 0, j))
        sign *= -1
    return det
