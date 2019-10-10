#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Manager, Queue, Pool
import os

def consumer_func(queue):
    d = {}
    total = 0
    while True:
        get = queue.get()
        if get == 'kill':
            break
        d.update(get)
    for key in d:
        total += d[key]
    d['total'] = total
    return d

def producer_func(queue, filename, path_to_dir):
     with open(path_to_dir+'/'+filename, 'r') as f:
        count = 0 
        for line in f:
            count += len(line.split())
        queue.put({filename: count})

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
    proc_num = 4
    pool = Pool(proc_num)
    queue = Manager().Queue()
    file_list = os.listdir(path=path_to_dir)
    print("file_list = ", file_list)
    result = pool.apply_async(consumer_func, (queue,))
    procs = []
    for file in file_list:
        proc = pool.apply_async(producer_func, (queue, file, path_to_dir))
        procs.append(proc)

    for proc in procs:
        proc.get()

    queue.put('kill')
    return result.get()
