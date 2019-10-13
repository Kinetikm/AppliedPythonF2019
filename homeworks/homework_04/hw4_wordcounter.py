#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
from os import listdir


def words_counter(path_to_file, filename, output):
    cnt = 0
    with open(path_to_file + '/' + filename) as file:
        for line in file:
            cnt += len(line.split())
        file.close()
    output[filename] = cnt
    output["total"] += cnt


def word_count_inference(path_to_dir):
    man = Manager()
    output = man.dict({"total": 0})

    q = []
    for file in listdir(path_to_dir):
        p = Process(target=words_counter(path_to_dir, file, output))
        q.append(p)
        p.start()

    for el in q:
        el.join()
    return output
