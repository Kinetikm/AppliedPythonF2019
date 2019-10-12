#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Pool, Manager, Queue
import os


def counter(file_name, word_dict):
    counter_word = 0
    with open(file_name, 'r') as f:
        for line in f:
            counter_word += len(line.split())
    word_dict.update({file_name: counter_word})


def word_count_inference(path_to_dir):
    manager = Manager()
    tmp_queue = manager.Queue()
    tmp_dict = manager.dict()
    pool = Pool(3)
    for i in os.listdir(path_to_dir):
        tmp_queue.put(path_to_dir + "/" + i)
    tmp_queue.put("end")
    while True:
        a = tmp_queue.get()
        if a == "end":
            break
        p = pool.apply_async(counter, (a, tmp_dict))
        p.get()
    tmp_queue.put("Happy end")
    summ = 0
    for key in tmp_dict:
        summ += tmp_dict[key]
    tmp_dict.update({total: summ})
    result = dict(tmp_dict)
    return result
