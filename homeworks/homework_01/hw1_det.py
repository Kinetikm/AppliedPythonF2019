#!/usr/bin/env python
# coding: utf-8


def next_perm(perm):
    n = len(perm)
    i = n-2
    while True:
        if i < 0:
            raise ValueError
        if perm[i] < perm[i+1]:
            break
        i -= 1
    help_bool = bool((1 + (n-i-1)//2) % 2)
    j = n-1
    while j > i and perm[i] > perm[j]:
        j -= 1
    perm[i], perm[j] = perm[j], perm[i]
    i += 1
    j = n-1
    while i < j:
        perm[i], perm[j] = perm[j], perm[i]
        i += 1
        j -= 1
    return help_bool


def calculate_determinant(list_of_lists):
    for lst in list_of_lists:
        if len(lst) != len(list_of_lists):
            return None
    n = len(list_of_lists)
    det = 0
    perm = list(range(n))
    inv_fact = 1
    while True:
        term = 1
        for i in range(n):
            term *= list_of_lists[i][perm[i]]
        det += inv_fact*term
        try:
            help_bool = next_perm(perm)
            if help_bool:
                inv_fact *= -1
        except ValueError:
            break
    return det
