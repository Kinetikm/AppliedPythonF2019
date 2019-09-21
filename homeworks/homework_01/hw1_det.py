#!/usr/bin/env python
# coding: utf-8

def calculate_determinant(A):
    import copy
    M, N, Det = len(A), len(A[0]), 0
    if M != N: return None
    if N == 1: return A[0][0]
    for i in range(N):
        Minor = copy.deepcopy(A)
        del Minor[0]
        for j in range(1, len(A[0])):
            del Minor[j - 1][i]
        if i % 2 == 0:
            Det += A[0][i] * calculate_determinant(Minor)
        else:
            Det -= A[0][i] * calculate_determinant(Minor)
    return Det








