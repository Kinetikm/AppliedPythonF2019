#!/usr/bin/env python
# coding: utf-8


import os
from multiprocessing import Process, Manager
import time

class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, function, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
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
    def __init__(self, tasks_queue, result_queue, is_returnable):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        super(TaskProcessor, self).__init__()
        self._tasks_queue = tasks_queue
        self._result_queue = result_queue
        self._is_returnable = is_returnable

    def run(self):
        """
        Старт работы воркера
        """
        time.sleep(3)
        print(f'I\'m {os.getpid()} and i still alive')
        result = self._tasks_queue.get().perform()
        if self._is_returnable:
            self._result_queue.put(result)


class TaskManager(Process):
    """
    Мастер-процесс, который управляет воркерами
    """
    def __init__(self, tasks_queue, result_queue, n_workers, timeout=0, is_returnable=False):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """
        super(TaskManager, self).__init__()
        self._tasks_queue = tasks_queue
        self._result_queue = result_queue
        self._n_workers = n_workers
        self._is_returnable = is_returnable
        
        self._list_workers = []

    def run(self):
        """
        Запускайте бычка! (с)
        """
        while True:
            while len(self._list_workers) != self._n_workers:
                worker = TaskProcessor(self._tasks_queue, self._result_queue, self._is_returnable)
                self._list_workers.append(worker)
                worker.start()
                print(f'I\'m boss and i create new process {worker.pid}')
            for i, process in enumerate(self._list_workers):
                if not(process.is_alive()):
                    self._list_workers.pop(i)