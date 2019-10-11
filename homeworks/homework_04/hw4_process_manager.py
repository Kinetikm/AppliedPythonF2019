#!/usr/bin/env python
# coding: utf-8

import multiprocessing as mp
from multiprocessing import Process


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, something):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.something = something
        #raise NotImplementedError

    def perform(self):
        """
        Старт выполнения задачи
        """
        print("something happend...")
        return self.something
        #raise NotImplementedError


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue
        #raise NotImplementedError

    def run(self):
        """
        Старт работы воркера
        """
        try:
            task = self.tasks_queue.get()
        except:
            print("end has been reached")
        job = Process(target=task.perform())
        job.start()
        return job
        #raise NotImplementedError


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
        self.tasks_queue = mp.Manager.Queue()
        self.n_workers = n_workers
        self.timeout = timeout
        #raise NotImplementedError

    def run(self):
        """
        Запускайте бычка! (с)
        """
        flag = self.tasks_queue.empty()
        while flag != True:
            tasks = []
            len_of_queue = self.tasks_queue.qsize()
            tasks = [TaskProcessor(self.tasks_queue).run() for i in xrange(n_workers)]
            for task in tasks:
                task.join(timeout)
        #raise NotImplementedError
