#!/usr/bin/env python
# coding: utf-8


def perestanovki(a, p, k=0):
    if k == len(a):
        p.append(a[:])
    else:
        for i in range(k, len(a)):
            a[k], a[i] = a[i], a[k]
            perestanovki(a, p, k + 1)
            a[k], a[i] = a[i], a[k]
    return p


# факториал

def factorial(n):
    fact = 1
    while n > 0:
        fact = fact * n
        n -= 1
    return fact


# количество перестановок
def f(a):
    k = 0
    for i in range(len(a)):
        j = i + 1
        while j < len(a):
            if a[i] > a[j]:
                k += 1
            j += 1
    return k


def calculate_determinant(list_of_lists):
    n = len(list_of_lists)
    print('list    ', list_of_lists)
    if n != 0:
        if (n == 1) and (len(list_of_lists[n - 1]) == 1):
            return list_of_lists[0][0]
        # если не квадратная
        if n != len(list_of_lists[n - 1]):
            return None
        else:
            p = perestanovki(a=[i for i in range(n)], p=[])
            print('перестановки      ', p)
            det = 0
            for i in range(factorial(n)):
                x = 1
                for j in range(n):
                    x = x * list_of_lists[j][p[i][j]]
                k = f(p[i])
                det = det + ((-1) ** k) * x
        return det
    else:
        return None
