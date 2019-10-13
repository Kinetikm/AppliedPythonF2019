#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
from time import sleep, time
import os


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, func, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.args = args
        self.kwargs = kwargs
        self.func = func

    def perform(self):
        """
        Старт выполнения задачи
        """
        self.func(*self.args, **self.kwargs)


class TaskProcessor:

    def __init__(self, tasks_queue):
        self.tasks_queue = tasks_queue
        self.time = 0

    def run(self):
        Task = self.tasks_queue.get()
        self.process = Process(target=Task.perform, args=())
        self.process.start()
        self.time = time()


class TaskManager:
    def __init__(self, tasks_queue, n_workers, timeout):
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.work = []

    def run(self):
    """
    Запускайте бычка! (с)
    """
        for _ in range(self.n_workers):
            worker = TaskProcessor(self.tasks_queue)
            self.work.append(worker)
            worker.run()
        while not self.tasks_queue.empty():
            for curwork in self.work:
                if curwork.process.is_alive():
                    if time() - curwork.time > self.timeout:
                        del curwork
                        if not self.tasks_queue.empty():
                            worker = TaskProcessor(self.tasks_queue)
                            self.work.append(worker)
                            worker.run()
                else:
                    del curwork
                    if not self.tasks_queue.empty():
                        worker = TaskProcessor(self.tasks_queue)
                        self.work.append(worker)
                        worker.run()
        while len(self.work) != 0:
            for curwork in self.work:
                if curwork.process.is_alive():
                    if time() - curwork.time > self.timeout:
                        del curwork
                else:
                    del curwork


def sqr(n):
    sleep(1)
    if n == 0:
        print(0)
        return 0
    res = 1
    for i in range(1, n+1):
        res *= i
    print(res)
    return res


if __name__ == '__main__':
    q = Queue()
    n_workers_ = 4
    timeout_ = 6
    tasks = 20

    for j in range(tasks):
        q.put(Task(sqr, j))

    manager = TaskManager(q, n_workers_, timeout_)
    manager.run()
