#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Manager, Pool
import os


def count_of_words(file_path, queue, words=0):
    with open(file_path, 'r') as f:
        for line in f:
            words += len(line.split())
    path_word = {os.path.split(file_path)[1]: words}
    queue.put(path_word)


def consumer_func(queue):
    my_dic, total_words = {}, 0
    while 1:
        res = queue.get()
        if res == 'kill':
            break
        my_dic.update(res)
    for key in my_dic:
        total_words += my_dic[key]
    my_dic['total'] = total_words
    return my_dic


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

    num_of_proc = 2
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(num_of_proc)
    files = os.listdir(path_to_dir)
    res = pool.apply_async(consumer_func, (queue,))
    for file in files:
        process = pool.apply_async(count_of_words, (path_to_dir+'/'+file, queue))
        process.get()
    queue.put('kill')
    return res.get()