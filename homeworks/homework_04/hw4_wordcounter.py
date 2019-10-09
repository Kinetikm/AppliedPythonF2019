#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
import os


def words_in_file(path_to_dir, filename, queue):
    sum = 0
    temp_set = ()
    with open(path_to_dir + "/" + filename, 'r') as f:
        sum = len(f.read().strip().split())
    temp_set = (filename, sum)
    queue.put(temp_set)


def queue_switching(queue):
    total = 0
    major_dict = {}
    while True:
        res = queue.get()
        if res == 'kill':
            break
        total += res[1]
        major_dict[res[0]] = res[1]
    major_dict['total'] = total
    return major_dict


def word_count_inference(path_to_dir):
    PROCESSES_COUNT = os.cpu_count()
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(PROCESSES_COUNT)
    tasks = pool.apply_async(queue_switching, (queue, ))
    jobs = []
    for filename in os.listdir(path_to_dir):
        if os.path.isfile(path_to_dir + '/' + filename):
            job = pool.apply_async(words_in_file, (path_to_dir, filename, queue))
            jobs.append(job)

    for job in jobs:
        job.get()

    queue.put('kill')
    done_tasks = tasks.get()
    pool.close()
    pool.join()
    return done_tasks
