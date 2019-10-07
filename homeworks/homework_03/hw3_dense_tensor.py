#!/usr/bin/env python
# coding: utf-8


class Tensor:
    """
    Your realisation of numpy tensor.

    Must be implemented:
    1. Getting and setting element by indexes of row and col.
    a[i, j] = v -- set value in i-th row and j-th column to value.
    b = a[i, j] -- get value from i-th row and j-th column.
    2. Pointwise operations.
    c = a + b -- sum of two Tensors of the same shape or sum with scalar.
    c = a - b -- difference --//--.
    c = a * b -- product --//--.
    c = a / alpha -- divide Tensor a by nonzero scalar alpha.
    c = a ** b -- raises each element of a to the power b.
    3. Sum, mean, max, min, argmax, argmin by axis.
    if axis is None then operation over all elements.
    4. Transpose by given axes (by default reverse dimensions).
    5. Swap two axes.
    6. Matrix multiplication for tensors with dimension <= 2.
    """

    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: list of lists
        """

        self._matrix = init_matrix_representation
        self.shape = ()
        self._calc_shape()
        raise NotImplementedError

    def _calc_shape(self, next_dim=None):
        if next_dim is None:
            next_dim = self._matrix

        self.shape = (*list(self.shape), len(next_dim),)

        if isinstance(next_dim[0], list):
            self._calc_shape(next_dim=next_dim[0])
        else:
            # print("calllcing shape", self.shape)
            self._check_shape()
        return

    def _check_shape(self, dim=0, matrix=None):
        if dim >= len(self.shape):
            return
        if matrix is None:
            matrix = [self._matrix]

        for i in matrix:
            assert len(i) == self.shape[dim]
            self._check_shape(dim=dim+1, matrix=i)

        return

    def _apply(self, func: callable):
        key = self.shape[:-1]
        m = self._matrix
        for i in range(key[:-1]):
            m = m[i]

        for i in range(key[-1]):
            idx = (*list(key[:-1]), i)
            m[i] = func(m[i], idx=idx)

        return

    def __matmul__(self, other):
        pass

    def __add__(self, other):
        if not isinstance(other, Tensor):
            self._apply(lambda x: x + other)

        if self.shape != other.shape:
            raise ValueError()

        def mult_tensors(x, idx=None):
            return x + other[idx]
        self._apply(mult_tensors)

    def __sub__(self, other):
        if not isinstance(other, Tensor):
            self._apply(lambda x: x - other)

        if self.shape != other.shape:
            raise ValueError()

    def __mul__(self, other):
        pass

    def __getitem__(self, key):
        # print("getting:", key)
        m = self._matrix
        for i in key:
            m = m[i]
        return m

    def __setitem__(self, key, value):
        # print("assigment:", key, value)

        m = self._matrix
        for i in key[:-1]:
            m = m[i]
        m[key[-1]] = value
        return
