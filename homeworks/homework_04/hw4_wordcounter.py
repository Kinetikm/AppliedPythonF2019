#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Pool, Manager, cpu_count
import os
from collections import namedtuple


WordsInFile = namedtuple("WordsInFile", ["file", "num_words"])


def count_words_in_file(file_path, queue):
    with open(file_path) as file:
        num_words = len(file.read().split())
    queue.put(WordsInFile(file=file_path.split("/")[-1], num_words=num_words))


def count_total_words(queue):
    # Можно было бы сделать Manager().Dict() и передавать его вместе с очередью, но мне показалось такое решение лучше
    data_dict = {}
    count = 0
    while True:
        elem = queue.get()
        if elem == "kill":
            break
        count += elem.num_words
        data_dict[elem.file] = elem.num_words

    data_dict["total"] = count

    return data_dict


def word_count_inference(path_to_dir):
    """
    Метод, считающий количество слов в каждом файле из директории
    и суммарное количество слов.
    Слово - все, что угодно через пробел, пустая строка "" словом не считается,
    пробельный символ " " словом не считается. Все остальное считается.
    Решение должно быть многопроцессным. Общение через очереди.
    :param path_to_dir: путь до директории с файлами
    :return: словарь, где ключ - имя файла, значение - число слов +
        специальный ключ "total" для суммы слов во всех файлах
    """
    queue = Manager().Queue()
    files = [os.path.join(path_to_dir, file) for file in os.listdir(path_to_dir)]

    pool = Pool(cpu_count())

    prc = pool.apply_async(count_total_words, (queue,))

    processes = []
    for file in files:
        process = pool.apply_async(count_words_in_file, (file, queue))
        processes.append(process)

    for process in processes:
        process.get()

    queue.put("kill")
    pool.close()
    pool.join()

    return prc.get()
