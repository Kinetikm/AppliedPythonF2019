#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
import time


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
        self.func(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self._queue = tasks_queue
        self.job = None
        self.time = None

    def run(self):
        """
        Старт работы воркера
        """
        task = self._queue.get()
        try:
            self.time = time.time()
            self.job = Process(target=task.perform)
            self.job.start()
        except TypeError:
            raise TypeError

    def time(self):
        return self.time

    def kill(self):
        self.job.terminate()
        self.job.join()


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
        self._queue = tasks_queue
        self.workers = n_workers
        self.timeout = timeout
        self.workers_lst = []
        self.workers_start_time = []

    def run(self):
        """
        Запускайте бычка! (с)
        """
        while not self._queue.empty() or self.workers_lst:
            if self._queue.empty() is False:
                while len(self.workers_lst) < self.workers:
                    task = TaskProcessor(self._queue)
                    self.workers_lst.append(task)
                    self.workers_lst.append(task)
                    self.workers_start_time.append(task.time)
                    task.run()
                    print(f"Process {} started", task.get_pid())
            for i in range(len(self.workers_lst)):
                if self.workers_lst[i].is_alive() is False:
                    print(f"Process {} killed", self.workers_lst[i].get_pid())
                    self.workers_lst[i].kill()
                    del self.workers_lst[i]
                    del self.workers_start_time[i]
            for i in range(len(self.workers_lst)):
                if time.time() - self.time_start[i] > self.timeout:
                    self.workers_lst[i].kill()
                    self.workers_lst.append()
                    print(f"Time of the process {} is over", self.workers_lst[i].get_pid())
