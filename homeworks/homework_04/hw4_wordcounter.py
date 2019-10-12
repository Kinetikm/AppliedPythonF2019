#!/usr/bin/env python
# coding: utf-8
from multiprocessing import Process, Manager, Pool
import os


def counter(list):  # list=[path, filename, queue
    number = 0
    dct = dict()
    with open(list[0] + '/' + list[1], 'r', encoding='utf-8') as file:
        for line in file:
            number += len(line.split())
    dct[list[1]] = number
    list[2].put(dct)


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
    files = os.listdir(path=path_to_dir)
    result = dict()
    sum = 0
    manager = Manager()
    queue = manager.Queue()
    forpool = Pool(4)  # сначала реализовал способ: для каждого файла свой процесс (4, потому что 4 ядра )
    mas = []  # но в беседе увидел, что надо небольшое количество процессов, поэтому переделал
    for file in files:
        mas.append([path_to_dir, file, queue])
    forpool.map(counter, mas)
    '''procs = []  # оставил старую реализацию
    for file in files:
        proc = Process(target=counter, args=([path_to_dir, file, queue],))  # пришлось обернуть в лист для новой реализ
        procs.append(proc)
        proc.start()'''

    while not queue.empty():
        res = queue.get()
        result.update(res)
        sum += list(res.values())[0]

    '''for process in procs:
        process.join()'''
    result['total'] = sum

    return result
