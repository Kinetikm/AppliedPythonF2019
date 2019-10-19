import numpy as np


def simplex_method(a, b, c):
    c *= -1
    a = a.astype(np.float)
    b = b.astype(np.float)
    c = c.astype(np.float)
    n, m = a.shape
    corr = -1*np.ones(n, dtype=np.int16)  # correspondence between var and row
    while True:
        c_min = np.min(c)
        if c_min >= 0:
            break
        pivot_col = np.argmin(c)
        pivot_row = np.argmin(b / a[:, pivot_col])
        pivot = a[pivot_row][pivot_col]
        b[pivot_row] /= pivot
        a[pivot_row] /= pivot
        for i in range(n):
            if i != pivot_row:
                b[i] -= b[pivot_row] * a[i][pivot_col]
                a[i] -= a[pivot_row] * a[i][pivot_col]
        c -= a[pivot_row]*c[pivot_col]
        corr[pivot_row] = pivot_col
    result = np.zeros(m)
    for i in range(n):
        if corr[i] != -1:
            result[corr[i]] = b[i]
    return result
