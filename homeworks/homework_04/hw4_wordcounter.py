#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Manager, Pool
import os


def sum_word(path, queue):  # суммирует слова в файле
    with open(path) as f:
        lines = 0
        words = 0
        letters = 0
        for line in f:
            lines += 1
            letters += len(line)
            pos = 'out'
            for letter in line:
                if letter != ' ' and pos == 'out' and letter != '\n':
                    words += 1
                    pos = 'in'
                elif letter == ' ':
                    pos = 'out'
    name = path.split('/')[-1]
    queue.put({name: words})


def total(queue):  # суммирует число слов в очереди
    tot = []
    w = {}
    while True:
        q = queue.get()
        if q == 'kill':
            break
        tot += q.values()
        w.update(q)
    finally_tot = sum(tot)
    w["total"] = finally_tot
    return w


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
    list_file = os.listdir(path=path_to_dir)
    manager = Manager()
    queue = manager.Queue()
    pool = Pool()
    result = pool.apply_async(total, (queue,))
    for file in list_file:
        full_path = path_to_dir + '/' + file
        proc = pool.apply_async(sum_word, (full_path, queue))
    proc.get()
    queue.put('kill')
    pool.close()
    pool.join()
    return result.get()
