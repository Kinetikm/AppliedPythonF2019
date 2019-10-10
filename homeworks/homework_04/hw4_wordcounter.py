#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import os


def read_file(path_to_dir, queue, d):
    filename = queue.get()
    word_list = []
    # print(filename, time.time(), os.getpid())
    full_name = str(path_to_dir) + '/' + str(filename)
    with open(full_name) as f:
        for line in f:
            word_list += [word for word in line.split()]
    d[filename] = len(word_list)


def word_count_inference(path_to_dir):
    manager = Manager()
    queue = manager.Queue()
    tasks = []
    d = manager.dict()
    for filename in os.listdir(path_to_dir):
        queue.put(filename)
        proc = Process(target=read_file, args=(path_to_dir, queue, d))
        tasks.append(proc)
        proc.start()
    for task in tasks:
        task.join()
    d['total'] = sum(d.values())
    return d
