# !/usr/bin/env python
# coding: utf-8

from multiprocessing import Manager, Process
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
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.status = "undone"

    def perform(self):
        """
        Старт выполнения задачи
        """
        self.function(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        if not tasks_queue.empty():
            temp = tasks_queue.get()
            if isinstance(temp, Task):
                self.task = temp
                self.process = Process(target=temp.perform())
                self.time = 0
            else:
                raise TypeError
        else:
            raise IndexError

    def run(self):
        """
        Старт работы воркера
        """
        self.process.start()
        self.time = time.time()


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
        self.workers = [-1] * n_workers

    def run(self):
        """
        Запускайте бычка! (с)
        """
        while not self.tasks_queue.empty():
            for i in self.workers:
                if i == -1:
                    i = TaskProcessor(self.tasks_queue)
                    i.run()
                    break
            for i in self.workers:
                if isinstance(i, TaskProcessor):
                    if time.time() - i.time > self.timeout:
                        i.terminate()
                        i.task.status = "timeout"
                        if not self.tasks_queue.empty():
                            i = TaskProcessor(self.tasks_queue)
                            i.run()
                    if not i.isAlive():
                        if not self.tasks_queue.empty():
                            i = TaskProcessor(self.tasks_queue)
                            i.run()






