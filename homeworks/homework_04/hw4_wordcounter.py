#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Pool, Manager
import os


def count_words(filename,  queue):
    cnt = 0
    with open(filename, 'r') as f:
        for line in f:
            lin = line.split()
            cnt += len(lin)
    queue.put({filename.split('/')[-1]: cnt})


def total_func(queue):
    res_map = {}
    total = 0
    while True:
        el = queue.get()
        if el == 'end':
            break
        total += list(el.values())[0]
        res_map.update(el)
    res_map['total'] = total
    return res_map


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
    manager = Manager()
    queue = manager.Queue()
    files = [os.path.join(path_to_dir, k) for k in os.listdir(path_to_dir)]
    pool = Pool(processes=len(files) + 1)
    w = pool.apply_async(total_func, (queue, ))
    res = [pool.apply_async(count_words, (filename, queue)) for filename in files]
    for r in res:
        r.get()
    queue.put('end')
    return w.get()
