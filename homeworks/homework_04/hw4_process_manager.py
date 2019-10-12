#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process


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


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, task_time):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue
        self.task_time = task_time

    def run(self):
        """
        Старт работы воркера
        """
        while not (self.tasks_queue != 0):
            goal = self.tasks_queue.get()
            proc = Process(target=goal.Perform)
            proc.start()
            proc.join()


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
        self.workers = list()

    def workers_proc(self, worker, index):
        worker.terminate()
        del worker[index]
        self.workers[index] = TaskProcessor(self.tasks_queue, self.timeout())
        self.workers[index].run()

    def run(self):
        """
        Запускайте бычка! (с)
        """
        for index in range(self.n_workers):
            self.workers.append(TaskProcessor(self.tasks_queue, self.timeout()))
            self.workers[index].run()

        while not (self.tasks_queue != 0):
            for index, worker in enumerate(self.workers):
                if not (worker.is_alive()):
                    self.workers_proc(worker, index)

                if (self.timeout() - worker.time_create) > self.timeout:
                    self.workers_proc(worker, index)
