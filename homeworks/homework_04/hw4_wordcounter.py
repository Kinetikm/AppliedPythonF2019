#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Queue, Pool
import os


def word_count_inference(path_to_dir):
    q = Queue()
    words = Manager().dict()
    tasks = []

    for file in os.listdir(path_to_dir):
        q.put(path_to_dir+'/'+file)

    files = os.listdir(path_to_dir)
    pool = Pool(5)
    result = pool.apply_async(f, args=(q, words))

    for i in files:
        p = pool.apply_async(f, args=(q, words))
        tasks.append(p)

    for task in tasks:
        task.get()

    pool.close()
    pool.join()

    words['total'] = sum(words.values())

    return words


def f(queue_of_files, words_in_file):
    try:
        while True:
            item = queue_of_files.get_nowait()
            if item is not None:
                with open(item, 'r') as f_id:
                    words_in_file[item.split('/')[-1]] = len(f_id.read().split())
            else:
                break
    except Exception as e:
        print(e)
