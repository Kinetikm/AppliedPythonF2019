#!/usr/bin/env python
# coding: utf-8
import random
import time

import numpy as np
import itertools

from homeworks.homework_03.hw3_hashmap import HashMap
from homeworks.homework_03.hw3_lrucache import LRUCacheDecorator
from homeworks.homework_03.hw3_csr_matrix import CSRMatrix
from homeworks.homework_03.hw3_dense_tensor import Tensor


def test_hashmap_01():
    try:
        hashmap = HashMap(10)
    except NotImplementedError:
        return True
    entries = [(5, 7), ("entries", 56), ("value", 54.), (1000, "t"), (HashMap(10), ())]
    for k, v in entries:
        assert hashmap._get_hash(k) == hash(k)
        assert hashmap._get_hash(v) == hash(v)
    for k, v in entries:
        assert hashmap._get_index(hashmap._get_hash(k)) == hash(k) % 10
        assert hashmap._get_index(hashmap._get_hash(v)) == hash(v) % 10


def test_hashmap_02():
    try:
        hashmap = HashMap(10)
    except NotImplementedError:
        return True
    entries = [(5, 7), ("entries", 56), ("value", 54.), (1000, "t"), (HashMap(10), ())]
    for k, v in entries:
        hashmap.put(k, v)
    assert len(hashmap) == 5
    for k, v in entries:
        hashmap.put(k, v)
    assert len(hashmap) == 5
    for k, v in entries:
        assert k in hashmap


def test_hashmap_03():
    try:
        hashmap = HashMap(10)
    except NotImplementedError:
        return True
    entries = [(5, 7), ("entries", 56), ("value", 54.), (1000, "t"), (HashMap(10), ())]
    inner_list_name = [k for k, v in hashmap.__dict__.items() if isinstance(v, list)][0]
    for k, v in entries:
        hashmap.put(k, v)
    for k, v in entries:
        assert HashMap.Entry(k, None) in hashmap.__dict__[inner_list_name][hashmap._get_index(hashmap._get_hash(k))]


def test_hashmap_04():
    try:
        hashmap = HashMap(10)
    except NotImplementedError:
        return True
    entries = [(5, 7), ("entries", 56), ("value", 54.), (1000, "t"), (HashMap(10), ()), ({"s": "v"}, {"v": "s"})]
    for k, v in entries:
        entry = HashMap.Entry(k, v)
        assert entry.get_key() == k
        assert entry.get_value() == v

    for i in range(len(entries)):
        entry_one = HashMap.Entry(entries[i][0], entries[i][1])
        for _ in range(10):
            j = random.randint(0, len(entries) - 1)
            p = random.randint(0, len(entries) - 1)
            entry_two = HashMap.Entry(entries[j][0], entries[p][1])
            if j == i:
                assert entry_one == entry_two
            else:
                assert entry_one != entry_two


def test_hashmap_05():
    try:
        hashmap = HashMap(10)
    except NotImplementedError:
        return True
    entries = [(5, 7), ("entries", 56), ("value", 54.), (1000, "t"), (HashMap(10), ())]
    for k, v in entries:
        hashmap.put(k, v)
    for k, v in entries:
        assert hashmap.get(k) == v
    for _ in range(100):
        i = random.randint(0, len(entries) - 1)
        j = random.randint(0, len(entries) - 1)
        hashmap.put(i, j)
        assert hashmap.get(i) == j
    assert hashmap.get("nexit", "default") == "default"


def test_hashmap_06():
    try:
        hashmap = HashMap(10)
    except NotImplementedError:
        return True
    entries = [(5, 7), ("entries", 56), ("value", 54.), (1000, "t"), (HashMap(10), ())]
    for k, v in entries:
        hashmap.put(k, v)
    output_values = set()
    output_keys = set()
    for v in hashmap.values():
        output_values.add(v)
    for k in hashmap.keys():
        output_keys.add(k)
    for k, v in entries:
        assert k in output_keys
        assert v in output_values
    output_values = set()
    output_keys = set()
    for k, v in hashmap.items():
        output_values.add(v)
        output_keys.add(k)
    for k, v in entries:
        assert k in output_keys
        assert v in output_values


def test_hashmap_07():
    try:
        hashmap = HashMap(2)
    except NotImplementedError:
        return True
    entries = [(5, 7), ("entries", 56), ("value", 54.), (1000, "t"), (HashMap(10), ())]
    for k, v in entries:
        hashmap.put(k, v)
    assert len(hashmap) == 5
    for k, v in entries:
        hashmap.put(k, v)
    assert len(hashmap) == 5
    for k, v in entries:
        assert k in hashmap


def test_lrucache_01():

    try:
        @LRUCacheDecorator(maxsize=3, ttl=None)
        def get_sq(s):
            time.sleep(2)
            return s ** 2
    except NotImplementedError:
        return True

    t_start = time.time()
    get_sq(1)
    assert time.time() - t_start > 0.5

    t_start = time.time()
    get_sq(1)
    assert time.time() - t_start < 0.5


def test_lrucache_02():
    try:
        @LRUCacheDecorator(maxsize=3, ttl=None)
        def get_sq(s):
            time.sleep(2)
            return s ** 2
    except NotImplementedError:
        return True

    get_sq(1)
    get_sq(2)
    get_sq(3)
    get_sq(1)
    get_sq(4)
    get_sq(5)

    t_start = time.time()
    get_sq(1)
    assert time.time() - t_start < 0.5


def test_lrucache_03():
    try:
        @LRUCacheDecorator(maxsize=4, ttl=None)
        def get_sq(s):
            time.sleep(1)
            return s ** 2
    except NotImplementedError:
        return True

    t_start = time.time()
    get_sq(1)
    assert time.time() - t_start > 0.5
    t_start = time.time()
    get_sq(1)
    assert time.time() - t_start < 0.5
    l = [5, 6, 7]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start > 0.5
    l = [1, 5, 6, 7]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start < 0.5
    l = [7, 5, 6, 1]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start < 0.5
    l = [15]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start > 0.5
    l = [1, 6, 5, 15]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start < 0.5
    l = [7]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start > 0.5


def test_lrucache_04():
    my_global_vars = {}
    try:
        @LRUCacheDecorator(maxsize=3, ttl=10)
        def get_sq(s):
            time.sleep(2)
            nonlocal my_global_vars
            my_global_vars[s] = s ** 2
            return my_global_vars[s]
    except NotImplementedError:
        return True

    get_sq(3)
    t_start = time.time()
    get_sq(3)
    assert time.time() - t_start < 2
    assert my_global_vars[3] == get_sq(3) == 9

    for i in my_global_vars:
        my_global_vars[i] += 1

    t_start = time.time()
    get_sq(3)
    assert time.time() - t_start < 2
    assert my_global_vars[3] != get_sq(3)

    time.sleep(10)
    get_sq(3)
    assert my_global_vars[3] == get_sq(3)


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


def test_tensor_get_item_method():
    np.random.seed(42)

    shapes = (20, 10, 20, 10)
    matrix = np.random.randint(0, 2, shapes)
    try:
        tensor = Tensor(matrix.tolist())
    except NotImplementedError:
        return True

    for ind in itertools.product(*[range(k) for k in shapes]):
        assert matrix[ind] == tensor[ind]


def test_tensor_set_item_method():
    np.random.seed(42)

    shapes = (20, 10, 20, 10)
    zero_matrix = np.zeros(shapes)
    matrix = np.random.randint(0, 3, shapes)
    try:
        tensor = Tensor(zero_matrix.tolist())
    except NotImplementedError:
        return True

    for ind in itertools.product(*[range(k) for k in shapes]):
        tensor[ind] = matrix[ind]

    for ind in itertools.product(*[range(k) for k in shapes]):
        assert matrix[ind] == tensor[ind]


def test_tensor_base_operations():
    np.random.seed(42)

    shapes = (20, 10, 20, 10)
    shapes2 = (20, 10, 20, 9)
    matrix1 = np.random.randint(-1, 2, shapes)
    matrix2 = np.random.randint(-1, 2, shapes)
    matrix3 = np.random.randint(-1, 2, shapes2)
    alpha = 2.5
    try:
        a = Tensor(matrix1.tolist())
        b = Tensor(matrix2.tolist())
        c = Tensor(matrix3.tolist())
    except NotImplementedError:
        return True

    flag = True
    try:
        a + c
        a - c
        a * c
        flag = False
    except ValueError:
        pass
    assert flag

    addition = a + b
    diff = a - b
    product = a * b

    addition_true = matrix1 + matrix2
    diff_true = matrix1 - matrix2
    product_true = matrix1 * matrix2

    for ind in itertools.product(*[range(k) for k in shapes]):
        assert addition[ind] == addition_true[ind]
        assert diff[ind] == diff_true[ind]
        assert product[ind] == product_true[ind]

    flag = True
    try:
        a / 0
        flag = False
    except ZeroDivisionError:
        pass
    assert flag

    addition = alpha + a
    diff = a - alpha
    product = a * alpha
    division = a / alpha
    pow = a ** 3

    addition_true = matrix1 + alpha
    diff_true = matrix1 - alpha
    product_true = matrix1 * alpha
    division_true = matrix1 / alpha
    pow_true = matrix1 ** 3

    for ind in itertools.product(*[range(k) for k in shapes]):
        assert addition[ind] == addition_true[ind]
        assert diff[ind] == diff_true[ind]
        assert product[ind] == product_true[ind]
        assert division[ind] == division_true[ind]
        assert pow[ind] == pow_true[ind]


def test_tensor_matmul():
    np.random.seed(42)

    shape_x, shape_y = 200, 300
    matrix1 = np.random.randint(-1, 2, (shape_x, shape_y))
    matrix2 = np.random.randint(-1, 2, (shape_y, shape_x))
    try:
        a = Tensor(matrix1.tolist())
        b = Tensor(matrix2.tolist())
        a1 = Tensor(matrix1[0].tolist())
        a2 = Tensor(matrix1[:, 0].tolist())
    except NotImplementedError:
        return True

    c = a @ b
    c1 = a @ a1
    c2 = a2 @ a
    c_true = matrix1 @ matrix2
    c1_true = matrix1 @ matrix1[0]
    c2_true = matrix1[:, 0] @ matrix1

    flag = True
    try:
        a @ a
        a @ a2
        a1 @ a
        flag = False
    except ValueError:
        pass
    assert flag

    for i, j in zip(range(c_true.shape[0]), range(c_true.shape[1])):
        assert c_true[i, j] == c[i, j]

    for i in range(c1_true.shape[0]):
        assert c1_true[i] == c1[i]

    for i in range(c2_true.shape[0]):
        assert c2_true[i] == c2[i]


def test_tensor_statistics():
    np.random.seed(42)

    shapes = (20, 10, 20, 10)
    matrix = np.random.randint(-20, 30, shapes)
    try:
        tensor = Tensor(matrix.tolist())
    except NotImplementedError:
        return True

    assert tensor.sum() == matrix.sum()
    assert tensor.mean() == matrix.mean()
    assert tensor.min() == matrix.min()
    assert tensor.max() == matrix.max()
    assert tensor.argmax() == matrix.argmax()
    assert tensor.argmin() == matrix.argmin()

    sum = tensor.sum(axis=2)
    mean = tensor.mean(axis=2)
    min = tensor.min(axis=2)
    max = tensor.max(axis=2)
    argmin = tensor.argmin(axis=2)
    argmax = tensor.argmax(axis=2)

    sum_true = matrix.sum(axis=2)
    mean_true = matrix.mean(axis=2)
    min_true = matrix.min(axis=2)
    max_true = matrix.max(axis=2)
    argmin_true = matrix.argmin(axis=2)
    argmax_true = matrix.argmax(axis=2)

    for ind in itertools.product(*[range(k) for k in sum_true.shape]):
        assert sum[ind] == sum_true[ind]
        assert mean[ind] == mean_true[ind]
        assert min[ind] == min_true[ind]
        assert max[ind] == max_true[ind]
        assert argmin[ind] == argmin_true[ind]
        assert argmax[ind] == argmax_true[ind]


def test_tensor_transpose():
    np.random.seed(42)

    shapes = (20, 10, 20, 10)
    matrix = np.random.randint(-20, 30, shapes)
    try:
        tensor = Tensor(matrix.tolist())
    except NotImplementedError:
        return True

    s = tensor.transpose(2, 0, 3, 1)
    s_true = matrix.transpose(2, 0, 3, 1)
    s1 = tensor.swapaxes(2, 0)
    s1_true = matrix.swapaxes(2, 0)

    for ind in itertools.product(*[range(k) for k in s_true.shape]):
        assert s[ind] == s_true[ind]

    for ind in itertools.product(*[range(k) for k in s1_true.shape]):
        assert s1[ind] == s1_true[ind]
