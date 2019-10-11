#!/usr/bin/env python
# coding: utf-8

import multiprocessing
import os


class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):

        while True:
            temp_task = self.task_queue.get()

            if temp_task is None:
                self.task_queue.task_done()
                break

            answer = temp_task.process()
            self.task_queue.task_done()
            self.result_queue.put(answer)


class Task():
    def __init__(self, name_file, path_to_dir):
        self.name_file = name_file
        self.path_to_dir = path_to_dir

    def process(self):
        with open(self.path_to_dir + '/' + self.name_file, 'r') as f:
            length = len(f.read().split())

        return self.name_file, length


def word_count_inference(path_to_dir='./test_data'):
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    n_consumers = multiprocessing.cpu_count()
    consumers = [Consumer(tasks, results) for i in range(n_consumers)]

    for consumer in consumers:
        consumer.start()
    files = os.listdir(path_to_dir)
    for item in files:
        tasks.put(Task(item, path_to_dir))

    for i in range(n_consumers):
        tasks.put(None)

    tasks.join()

    answer = {}
    sum = 0
    for _ in range(len(files)):
        temp_result = results.get()
        answer[temp_result[0]] = temp_result[1]
        sum += temp_result[1]
    answer['total'] = sum

    return answer
