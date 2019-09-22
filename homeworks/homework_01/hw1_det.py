#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(b):
    if len(b) <=1:
        return
    if len(b) != len(b[0]):
        return
    if len(b) == 2:
        de = b[0][0] * b[1][1] - b[0][1] * b[1][0]
        return de
    else:
        sum = 0
        for j in range(len(b)):
            c = [[0 for i in range(len(b)-1)] for j in range(len(b)-1)]
            i = 0
            for l in range(i+1, len(b)):
                for k in range(0, j):
                    c[l-i-1][k] = b[l][k]
                if j+1 == len(b):
                    for m in range(j+1, len(b)):
                        c[l-i-1][m-j+1] = b[l][m]
                elif j == 0:
                    for m in range(j+1, len(b)):
                        c[l-i-1][m-j-1] = b[l][m]
                else:
                    for m in range(j+1, len(b)):
                        c[l-i-1][m-1] = b[l][m]
            sum += b[i][j]*((-1)**j)*calculate_determinant(c)
        return sum
