#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(A):
    M, N, D = len(A), len(A[0]), 0
    if M != N:
        return None
    if N == 1:
        return A[0][0]
    for i in range(N):
        Minor = []
        for p in range(len(A)):
            Minor.append([])
            for k in range(len(A[0])):
                Minor[p].append(A[p][k])
        del Minor[0]
        for j in range(1, len(A[0])):
            del Minor[j - 1][i]
        if i % 2 == 0:
            D += A[0][i] * calculate_determinant(Minor)
        else:
            D -= A[0][i] * calculate_determinant(Minor)
    return D
