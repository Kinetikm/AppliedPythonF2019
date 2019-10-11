#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import time
import os


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, func, *args, **kwargs):
        #def wrapped(*args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        print(self.func(*self.args, **self.kwargs))


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue

    def run(self):
        """
        Старт работы воркера
        """
        while True:
            if not self.tasks_queue.empty():
                task = self.tasks_queue.get()
                print('my pid is ', os.getpid())
                task.perform()
            else:
                break


class TaskManager:
    """
    Мастер-процесс, который управляет воркерами
    """
    def __init__(self, tasks_queue, n_workers, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout


    def run(self):
        """
        Запускайте бычка! (с)
        """
        workers_lst = []
        while not self.tasks_queue.empty():
            if len(workers_lst) < self.n_workers:
                new_worker = TaskProcessor(self.tasks_queue)
                new_proc = Process(target=new_worker.run)
                workers_lst.append((new_proc, time.time()))
                new_proc.start()
            for i, val in enumerate(workers_lst):
                if time.time() - val[1] >= self.timeout:
                    val[0].terminate()
                    val[0].join()
                    del workers_lst[i]
                else:
                    break
                    
def f():
    time.sleep(1)
    return 2 ** 2

queue = Manager().Queue()
tasks = [Task(f) for i in range(7)]
for i in tasks:
    queue.put(i)
t = TaskManager(queue, 5, 5)
t.run()
