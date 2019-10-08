#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Manager, Pool
import os


def count_words_in_file(file_path, queue):
    words = 0
    with open(file_path, 'r') as file:
        for line in file:
            words += len(line.split())
    queue.put({os.path.basename(file_path): words})


def consumer_func(queue):
    my_map = {}
    total = 0
    while True:
        res = queue.get()
        if res == 'kill':
            break
        my_map.update(res)
    for key in my_map:
        total += my_map[key]
    my_map['total'] = total
    return my_map


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
    num_of_proc = 5
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(num_of_proc)
    file_names = os.listdir(path_to_dir)
    res = pool.apply_async(consumer_func, (queue,))
    for file in file_names:
        job = pool.apply_async(count_words_in_file, (path_to_dir+'/'+file, queue))
        job.get()
    queue.put('kill')
    return res.get()
