#!/usr/bin/env python
# coding: utf-8

import numpy as np


def simplex_method(a, b, c):
    """
    Почитать про симплекс метод простым языком:
    * https://ru.wikibooks.org/wiki/Симплекс-метод._Простое_объяснение
    Реализацию алгоритма взять тут:
    * https://youtu.be/gRgsT9BB5-8 (это ссылка на 1-ое из 5 видео).

    Используем numpy и, в целом, векторные операции.

    a * x.T <= b
    c * x.T -> max
    :param a: np.array, shape=(n, m)
    :param b: np.array, shape=(n, 1)
    :param c: np.array, shape=(1, m)
    :return x: np.array, shape=(1, m)
    """
    ans = np.zeros(a.shape[1])
    x = np.zeros(max(a.shape[1], a.shape[0]))
    e = np.eye(len(a) + 1)
    b_sim_matrix = np.hstack((b, 0)).reshape(len(b) + 1, 1)
    matrix = np.hstack((np.vstack((a, (-1 * c))), e))
    sim_matrix = np.hstack((matrix, b_sim_matrix))
    while min(sim_matrix[-1, :]) < 0:
        lead_col = sim_matrix[-1, :].argmin()
        lead_row = (sim_matrix[:-1, -1] / sim_matrix[:-1, lead_col]).argmin()
        key_element = sim_matrix[lead_row, lead_col]
        sim_matrix[lead_row, :] = sim_matrix[lead_row, :] / key_element
        for i in range(sim_matrix.shape[0]):
            if i != lead_row:
                sim_matrix[i, :] = sim_matrix[i, :] - \
                                   sim_matrix[lead_row, :] * sim_matrix[i, lead_col]
        x[lead_row] = lead_col + 1
    for i in range(len(x)):
        if int(x[i]) != 0:
            ans[int(x[i]) - 1] = sim_matrix[i, -1]
    return ans
