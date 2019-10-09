#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Manager, Pool
import os


def word_counter(filepath, queue):
    words = 0
    ins = False
    with open(filepath) as f:
        for line in f:
            words += len(line.split())
    filename = filepath.split("/")[-1]
    queue.put((filename, words))


def total_words(queue):
    res_dict = {}
    total = 0
    while True:
        w = queue.get()
        if w == "poison pill":
            break
        total += w[1]
        res_dict[w[0]] = w[1]
    res_dict["total"] = total
    return res_dict


def word_count_inference(path_to_dir):
    filepaths = [os.path.join(path_to_dir, file) for file in os.listdir(path_to_dir)]
    pool = Pool()
    manager = Manager()
    queue = manager.Queue()
    d = pool.apply_async(total_words, (queue,))
    for filepath in filepaths:
        result = pool.apply_async(word_counter, (filepath, queue))
    result.get()
    queue.put("poison pill")
    dictionary = d.get()
    pool.close()
    return dictionary
