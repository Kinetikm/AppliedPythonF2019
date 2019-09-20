#!/usr/bin/env python
# coding: utf-8
import copy
import random


def new_matrix(o_matr,column):
    n_matr = copy.deepcopy(o_matr)
    del n_matr[column:column + 1:1]
    for i in range(len(n_matr)):
        del n_matr[i][:1]
    return n_matr


def recrs(matr):
    det=0
    if len(matr) == 2:
        return matr[0][0]*matr[1][1]-matr[1][0]*matr[0][1]
    else:
        for pos in range(len(matr)):
            print(matr)
            if pos % 2 == 0:
                det += matr[pos][0]*recrs(new_matrix(matr, pos))
            else:
                det -= matr[pos][0]*recrs(new_matrix(matr, pos))
        print(det)
        return det


def calculate_determinant(list_of_lists):
    if len(list_of_lists) != len(list_of_lists[0]):
        return None
    if len(list_of_lists) == 1:
        return list_of_lists[0][0]
    else:
        return recrs(list_of_lists)
