import numpy as np


def simplex_method(a, b, c):
    simplex_table = np.hstack((np.hstack((b.reshape(b.shape[0], 1), a)), np.eye(len(b))))
    simplex_dif = np.hstack((np.hstack((np.array([0]), np.array(c))), np.array([0] * len(b))))
    simplex_table = np.vstack((simplex_table, simplex_dif))
    basis = np.array([i for i in range(len(a[0]), len(a[0]) + len(a))])
    while np.max(simplex_table[-1, :]) > 0:
        col_num = np.argmax(simplex_table[-1])
        if max(simplex_table[:, col_num]) <= 0:
            return None  # Нет решения
        row_num = np.argmax(simplex_table[:-1, col_num] / simplex_table[:-1, 0])
        new_matrix = np.copy(simplex_table)

        def func_1(x):
            return x / simplex_table[row_num, col_num]

        vec_1 = np.vectorize(func_1)
        for i in range(len(simplex_table)):
            if i == row_num:
                new_matrix[i] = vec_1(simplex_table[i])
            else:
                for j in range(len(new_matrix[i])):
                    new_matrix[i, j] -= simplex_table[row_num, j] * \
                                        simplex_table[i, col_num] / simplex_table[row_num, col_num]
        simplex_table = new_matrix
        basis[row_num] = col_num - 1
    res = np.zeros(len(basis))
    for i in range(len(basis)):
        if basis[i] < len(basis):
            res[basis[i]] = simplex_table[i, 0]
    return res
