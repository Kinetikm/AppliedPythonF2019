#!/usr/bin/env python
# coding: utf-8


import os
from multiprocessing import Process, Manager


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, function, *args, **kwargs):
        """
        :param function: функция, которая что-то делает
        :param args, kwargs: аргументы функции
        :return: результат выполнения данной функции
        """
        self._function = function
        self._args = args
        self._kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        return self._function(*self._args, **self._kwargs)


class TaskProcessor(Process):
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        super(TaskProcessor, self).__init__()
        self._tasks_queue = tasks_queue

    def run(self):
        """
        Старт работы воркера
        """
        res = self._tasks_queue.get()
        res.perform()


class TaskManager(Process):
    """
    Мастер-процесс, который управляет воркерами
    """
    def __init__(self, tasks_queue, n_workers, timeout=0):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """
        super(TaskManager, self).__init__()
        self._tasks_queue = tasks_queue
        self._n_workers = n_workers
        self._timeout = timeout
        self._list_workers = []

    def run(self):
        """
        Запускайте бычка! (с)
        """
        while self._tasks_queue.qsize():
            while len(self._list_workers) != self._n_workers:
                worker = TaskProcessor(self._tasks_queue)
                self._list_workers.append(worker)
                worker.start()
            for i, process in enumerate(self._list_workers):
                if not(process.is_alive()):
                    self._list_workers.pop(i)
