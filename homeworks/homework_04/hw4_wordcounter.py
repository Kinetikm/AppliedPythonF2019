#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Pool, Manager, Queue
import os


def ich_queue(queue):
    ich_dict = dict()
    total = 0
    while True:
        data = queue.get()
        if data == 'zero':
            break
        ich_dict.update(data)
    for key in ich_dict:
        total += ich_dict[key]
    ich_dict['total'] = total
    return ich_dict


def ich_counter(path_to_dir, filename, queue):
    with open(path_to_dir+'//'+filename, 'r', encoding="utf-8") as file:
        count_word = 0
        for lines in file:
            count_word += len(lines.split())
        queue.put({filename: count_word})


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
    files = os.listdir(path_to_dir)
    queue = Manager().Queue()
    num_proc = len(files)
    pool = Pool(num_proc)
    result = pool.apply_async(ich_queue, (queue,))
    pr = list()
    for file in files:
        num_proc = pool.apply_async(ich_counter, (path_to_dir, file, queue))
        pr.append(num_proc)

    for num_proc in pr:
        num_proc.get()

    queue.put('zero')
    return result.get()
