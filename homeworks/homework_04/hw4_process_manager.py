#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
from time import time, sleep


class Task:
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def perform(self):
        self.func(*self.args)


class TaskProcessor:
    def __init__(self, tasks_queue, tmeout, n_o_w):
        self.process = None
        self.timeout = tmeout
        self.queue = tasks_queue
        self.now = n_o_w

    def run(self):
        while not self.queue.empty():
            task = self.queue.get()
            self.process = Process(target=task.perform)
            print("worker ", self.now, "got new task with args:", task.args)
            self.process.start()
            self.process.join(timeout=self.timeout)
            self.process.terminate()


class TaskManager:
    def __init__(self, tasks_queue, n_workers, tmeout):
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = tmeout
        self.workers = []

    def run(self):
        for n_o_w in range(self.n_workers):
            self.workers.append(TaskProcessor(self.tasks_queue, self.timeout, n_o_w))
        processes = []
        for worker in self.workers:
            proc = Process(target=worker.run)
            processes.append(proc)
            proc.start()
        # reload if worker is not alive
        while not self.tasks_queue.empty():
            for n_o_w in range(self.n_workers):  # number of worker
                if not processes[n_o_w].is_alive():
                    processes[n_o_w].terminate()
                    self.workers[n_o_w] = TaskProcessor(self.tasks_queue, self.timeout, n_o_w)
                    proc = Process(target=self.workers[n_o_w].run)
                    processes[n_o_w] = proc
                    proc.start()


def t_func(a, c):
    sleep(a * 4)
    b = a * c * 10
    print("result of func with args (", a, ",", c, ") :", b)
    return b


if __name__ == '__main__':
    # test
    queue = Queue()
    n_workers_ = 3
    timeout = 15
    for i in range(10):
        queue.put(Task(t_func, i, i))
    manager = TaskManager(queue, n_workers_, timeout)
    manager.run()
# 0,1,3 got result; 4,5,6,7,9 finished cause of timeout


