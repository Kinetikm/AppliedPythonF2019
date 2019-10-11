#!/usr/bin/env python
# coding: utf-8


from multiprocessing import Process, Manager
import os


def func(path_to_dir, name_of_file, result):
    file = open(path_to_dir + os.sep + name_of_file, encoding='utf8')
    num_of_words = 0
    ch1 = file.read(1)
    while True:
        if not ch1:
            break
        ch2 = file.read(1)
        if not ch1.isspace() and (ch2.isspace() or not ch2):
            num_of_words += 1
        ch1 = ch2
    file.close()
    result[name_of_file] = num_of_words


def word_count_inference(path_to_dir):
    list_of_files = os.listdir(path=path_to_dir)
    manager = Manager()
    result = manager.dict()
    tasks = []
    len_max = 4  # максимальное количество запущенных процессов одновременно
    for name_of_file in list_of_files:
        task = Process(target=func, args=(path_to_dir, name_of_file, result))
        tasks.append(task)
        task.start()
        i = 0
        while len(tasks) == len_max:
            for i in range(len_max):
                if not tasks[i].is_alive():
                    tasks.pop(i)
                    break
    for task in tasks:
        task.join()
    tasks.clear()
    total = 0
    for i in result:
        total += result[i]
    result['total'] = total
    return result
