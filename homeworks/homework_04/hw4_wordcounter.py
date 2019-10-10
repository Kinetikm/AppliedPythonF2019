#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import os
from collections import deque
import codecs


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
    files_queue = manager.Queue()
    result = {"total": 0}
    files = os.listdir(path=path_to_dir)
    for filename in files:
        files_queue.put(filename)

    processes = deque()
    res_que = manager.Queue()
    while not files_queue.empty() > 0:
        for _ in range(4):
            proc = Process(target=read_file, args=(files_queue.get(), path_to_dir, res_que))
            processes.append(proc)
            proc.start()

    for proc in processes:
        proc.join()

    while not res_que.empty() > 0:
        couple = res_que.get()
        result[couple[0]] = couple[1]
        result['total'] += couple[1]
    print(result)
    return result


def read_file(filename, path_to_dir, res_que):
    path = path_to_dir + '/' + filename
    with codecs.open(path, 'r', 'utf_8_sig') as file:
        text = []
        word_num = 0
        for line in file:
            if line != '\n':
                text = line.split(' ')
                word_num += len(text)
        res_que.put([filename, word_num])
