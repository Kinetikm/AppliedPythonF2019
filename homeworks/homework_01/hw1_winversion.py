#!/usr/bin/env python
# coding: utf-8

def reverse_part(a, inl, size):
    for i in range((size - 1) // 2 + 1):
        tmp = a[inl+i]
        a[inl+i]=a[inl + size - (i + 1)]
        a[inl + size - (i + 1)] = tmp
    return a
#функция для того, чтобы перевернуть подмассив,
#начиная с inl, размером size

def word_inversion(a):
    if a == []:
        return a
    i = 0
    inl = 0
    #индекс начала подмассива, элементы которого образуют слово
    size = 0
    while True:
        if a[i].isalpha():
            inl = inl
            size += 1
            if (a[i] == a[-1]):
                reverse_part(a, inl, size)
                break
            i += 1
        #Просмотр элементов, содержащих буквенные символы/собирание слова
        else:
            reverse_part(a, inl, size)
            size = 0
            if a[i] == a[-1]:
                break
            i += 1
            inl = i
        #Просмотр элементов, не содержазих буквенные символы
    a.reverse()
    return a
    raise NotImplementedError
#основной метод - его суть в том, чтобы перестроить слова
#в обратном порядке, а потом и весь список



