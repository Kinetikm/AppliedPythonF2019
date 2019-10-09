#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Lock, Pool
import os
import sys

PROCESSES_COUNT = 5


def get_files_from_path(path) -> list:
    files_gen = os.walk(path)
    path_dirs_files = next(files_gen)
    files = path_dirs_files[2]
    return files


def get_words_count(file):
    with open(file) as f:
        text = f.read()
    lines = text.split('\n')
    plain_text = " ".join(lines)
    words = [word for word in plain_text.split(' ') if len(word) > 0]
    return len(words)


def consumer_func(path, queue, words_in_files):
    while True:
        filename = queue.get()
        if filename == 'kill':
            break
        words_count = get_words_count(f"{path}/{filename}")
        words_in_files[filename] = words_count
        # print(f"Wow,{os.getpid()} I found {filename} in queue with {words_count} words!")


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

    if not os.path.isdir(path_to_dir):
        sys.exit("Path is not a directory")

    manager = Manager()
    queue = manager.Queue()
    pool = Pool(PROCESSES_COUNT)
    words_in_files = manager.dict()

    files = get_files_from_path(path_to_dir)

    for file in files:
        queue.put(file)

    pool.apply_async(consumer_func, args=(path_to_dir, queue, words_in_files))

    queue.put('kill')

    pool.close()
    pool.join()

    words_in_files['total'] = sum(list(words_in_files.values()))
    return words_in_files
