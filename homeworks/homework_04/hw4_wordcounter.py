#!/usr/bin/env python
# coding: utf-8
from multiprocessing import Process, Manager
import os


def word_counter(path, file, files_and_amounts):
    try:
        with open(path + '/' + file, 'r', encoding='utf-8') as file_handler:
            number = len(file_handler.read().strip().split())
        files_and_amounts[file] = number
        if 'total' in files_and_amounts:
            files_and_amounts['total'] += number
        else:
            files_and_amounts['total'] = number
    except IOError:
        print("An IOError has occurred!")


def word_count_inference(path_to_dir):
    file_mas = os.listdir(path=path_to_dir)
    manager = Manager()
    files_and_amounts = manager.dict()
    queue = manager.Queue()
    files = []
    for file in file_mas:
        queue.put(file)
    while not queue.empty():
        file = queue.get()
        task = Process(target=word_counter, args=(path_to_dir, file, files_and_amounts))
        files.append(task)
        task.start()
    for task in files:
        task.join()
    return files_and_amounts
