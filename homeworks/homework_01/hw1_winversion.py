#!/usr/bin/env python
# coding: utf-8


def reverse_part(a, inl, size):
    for i in range((size - 1) // 2 + 1):
        tmp = a[inl+i]
        a[inl+i] = a[inl + size - (i + 1)]
        a[inl + size - (i + 1)] = tmp
    return a
# функция для того, чтобы перевернуть подмассив,
# начиная с inl, размером size


def word_inversion(a):
    i = 0
    inl = 0
    # индекс начала подмассива, элементы которого образуют слово
    size = 0
    print(i)
    print(inl)
    print(size)
    while True:
        if a[i].isalpha():
            size += 1
            if i == len(a) - 1:
                reverse_part(a, inl, size)
                break
            i += 1
            print(i)
            print(inl)
            print(size)
        # Просмотр элементов, содержащих буквенные символы/собирание слова
        else:
            if size > 0:
                reverse_part(a, inl, size)
                size = 0
            if i == len(a) - 1:
                break
            i += 1
            inl = i
            print(i)
            print(inl)
            print(size)          
        # Просмотр элементов, не содержазих буквенные символы
    a.reverse()
    return a
# основной метод - его суть в том, чтобы перестроить слова
# в обратном порядке, а потом и весь список
