#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Pool, Manager
import os


def word_counter(path_to_dir, file_name, q):
    file = open(f'{path_to_dir}/{file_name}', 'r')
    word_count = 0
    for line in file:
        word_list = line.split()
        word_count += len(word_list)
    pair = {file_name: word_count}
    q.put(pair)


def sum_dict(q):
    word_dict = {}
    while True:
        pair = q.get()
        if pair == 'break':
            break
        word_dict.update(pair)
    total = 0
    for key in word_dict:
        total += word_dict[key]
    word_dict['total'] = total
    return word_dict


def word_count_inference(path_to_dir):
    '''
    Метод, считающий количество слов в каждом файле из директории
    и суммарное количество слов.
    Слово - все, что угодно через пробел, пустая строка "" словом не считается,
    пробельный символ " " словом не считается. Все остальное считается.
    Решение должно быть многопроцессным. Общение через очереди.
    :param path_to_dir: путь до директории с файлами
    :return: словарь, где ключ - имя файла, значение - число слов +
        специальный ключ "total" для суммы слов во всех файлах
    '''
    q = Manager().Queue()
    pool = Pool(5)
    procs = []
    for file_name in os.listdir(path_to_dir):
        proc = pool.apply_async(word_counter, (path_to_dir, file_name, q,))
        procs.append(proc)
    for proc in procs:
        proc.get()
    q.put('break')
    pool.close()
    pool.join()
    return sum_dict(q)










