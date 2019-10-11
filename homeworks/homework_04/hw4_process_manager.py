#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Queue
from time import time, sleep

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
        self.func = func
        self.args = args
        self.kwargs = kwargs


    def perform(self):
        """
        Старт выполнения задачи
        """
        return self.func(*self.args, **self.kwargs)


class TaskProcessor(Process):
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, res_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        super().__init__()
        self.tasks_queue = tasks_queue
        self.res_queue = res_queue
        self.flag = 0

    def run(self):
        """
        Старт работы воркера
        """
        item = self.tasks_queue.get()
        res = item.perform()
        if res is not None:
            self.res_queue.put(res)
        else:
            self.res_queue.put('Function does not return anything!')


class TaskManager(Process):
    """
    Мастер-процесс, который управляет воркерами
    """
    def __init__(self, tasks_queue, res_queue, n_workers, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """
        super().__init__()
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.res_queue = res_queue


    def run(self):
        """
        Запускайте бычка! (с)
        """
        jobs = []
        times = []

        while True:
            print(len(jobs))
            sleep(1)
            while len(jobs) < self.n_workers:
                job = TaskProcessor(self.tasks_queue, self.res_queue)
                if self.tasks_queue.qsize():
                    flag = 1
                else:
                    flag = 0
                jobs.append(job)
                job.start()
                times.append([time(), flag])

            for i, job in enumerate(jobs):
                if times[i][1]:
                    if time() - times[i][0] > self.timeout:
                        jobs[i].kill()
                if not job.is_alive():
                    del jobs[i]
                    del times[i]
