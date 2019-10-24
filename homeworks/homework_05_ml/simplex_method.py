#!/usr/bin/env python
# coding: utf-8

import numpy as np


def simplex_method(a, b, c):
    matr = np.array(a, float)  # приводим входные к матрице, где самый последний столбец-b, а ласт строка -с
    matr = np.vstack((matr, -c))
    b = np.append(b, [0])
    b = b[:, np.newaxis]
    matr = np.hstack((matr, b))
    x_array = np.full((np.shape(a)[0]), -1)
    while (any(matr[-1] < 0)):
        colom = np.argmin(matr[-1])
        with np.errstate(divide='ignore'):  # это вставил, чтобы не выдавало RuntimeWarning
            row = (matr[:-1, -1] / matr[:-1, colom]).argmin()
        pivot_el = matr[row, colom]
        x_array[row] = colom
        matr[row] = matr[row] / pivot_el
        for i in range(np.shape(matr)[0]):  # цикл работы с матрицей
            if not (i == row):
                mnog = -(matr[i, colom] / matr[row, colom])
                matr[i] += matr[row] * mnog
    x = np.full((np.shape(a)[1]), 0)
    for i in range(len(x_array)):  # в x_array реализовано то, что было в видосе со вставкой x1/x2 в s1/s2
        index = x_array[i]
        if not (index == (-1)):
            x[index] = int(matr[i, -1])
    return x
