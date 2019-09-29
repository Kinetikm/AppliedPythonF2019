#!/usr/bin/env python
# coding: utf-8


import numpy as np
from homeworks.homework_03.csr_matrix import CSRMatrix


def test_csr_matrix_init_from_data_row_col():
    np.random.seed(42)

    matrix = np.random.randint(0, 2, (200, 200))
    data = []
    row_ind = []
    col_ind = []
    for i, j in zip(range(matrix.shape[0]), range(matrix.shape[1])):
        if matrix[i, j] != 0:
            data.append(matrix[i, j])
            row_ind.append(i)
            col_ind.append(j)

    try:
        csr_matrix = CSRMatrix((row_ind, col_ind, data))
    except NotImplementedError:
        return True

    for i, j in zip(range(matrix.shape[0]), range(matrix.shape[1])):
        assert np.isclose(matrix[i, j], csr_matrix[i, j])


def test_csr_matrix_get_item_method():
    np.random.seed(42)

    matrix = np.random.randint(0, 2, (200, 200))
    try:
        csr_matrix = CSRMatrix(matrix)
    except NotImplementedError:
        return True

    for i, j in zip(range(matrix.shape[0]), range(matrix.shape[1])):
        assert np.isclose(matrix[i, j], csr_matrix[i, j])


def test_csr_matrix_set_item_method():
    np.random.seed(42)

    zero_matrix = np.zeros((200, 200))
    matrix = np.random.randint(0, 3, (200, 200))
    try:
        csr_matrix = CSRMatrix(zero_matrix)
    except NotImplementedError:
        return True

    for i, j in zip(range(matrix.shape[0]), range(matrix.shape[1])):
        csr_matrix[i, j] = matrix[i, j]

    for i, j in zip(range(matrix.shape[0]), range(matrix.shape[1])):
        assert np.isclose(matrix[i, j], csr_matrix[i, j])


def test_csr_matrix_to_dense_method():
    np.random.seed(42)

    matrix = np.random.randint(0, 2, (200, 200))
    try:
        csr_matrix = CSRMatrix(matrix)
    except NotImplementedError:
        return True

    dense_matrix = csr_matrix.to_dense()

    for i, j in zip(range(matrix.shape[0]), range(matrix.shape[1])):
        assert np.isclose(matrix[i, j], dense_matrix[i, j])


def test_csr_matrix_nnz():
    np.random.seed(42)

    matrix = np.random.randint(0, 2, (200, 200))
    try:
        csr_matrix = CSRMatrix(matrix)
    except NotImplementedError:
        return True

    assert (matrix != 0).sum() == csr_matrix.nnz

    try:
        csr_matrix.nnz = -1
    except AttributeError:
        pass

    assert (matrix != 0).sum() == csr_matrix.nnz


def test_csr_matrix_base_operations():
    np.random.seed(42)

    shape_x, shape_y = 200, 200
    matrix1 = np.random.randint(-1, 2, (shape_x, shape_y))
    matrix2 = np.random.randint(-1, 2, (shape_x, shape_y))
    alpha = 2.5
    try:
        a = CSRMatrix(matrix1)
        b = CSRMatrix(matrix2)
    except NotImplementedError:
        return True

    addition = a + b
    diff = a - b
    product = a * b
    scalar = alpha * a
    division = a / alpha

    addition_true = matrix1 + matrix2
    diff_true = matrix1 - matrix2
    product_true = matrix1 * matrix2
    scalar_true = alpha * matrix1
    division_true = matrix1 / alpha

    assert (addition_true != 0).sum() == addition.nnz
    assert (diff_true != 0).sum() == diff.nnz

    for i, j in zip(range(shape_x), range(shape_y)):
        assert np.isclose(addition[i, j], addition_true[i, j])
        assert np.isclose(diff[i, j], diff_true[i, j])
        assert np.isclose(product[i, j], product_true[i, j])
        assert np.isclose(scalar[i, j], scalar_true[i, j])
        assert np.isclose(division[i, j], division_true[i, j])


def test_csr_matrix_matmul():
    np.random.seed(42)

    shape_x, shape_y = 200, 300
    matrix1 = np.random.randint(-1, 2, (shape_x, shape_y))
    matrix2 = np.random.randint(-1, 2, (shape_y, shape_x))
    try:
        a = CSRMatrix(matrix1)
        b = CSRMatrix(matrix2)
    except NotImplementedError:
        return True

    c = a @ b
    c_true = matrix1 @ matrix2

    assert (c_true != 0).sum() == c.nnz

    flag = True
    try:
        a @ a
        flag = False
    except ValueError:
        pass
    assert flag

    for i, j in zip(range(c_true.shape[0]), range(c_true.shape[1])):
        assert np.isclose(c_true[i, j], c[i, j])
