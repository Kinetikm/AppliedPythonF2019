#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process


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

    def perform(self):
        """
        Старт выполнения задачи
        """
        print("Start {}".format(function))
        function(*self.args, **self.kwargs)
        print("Done {}".format(function))


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue
        self.timeout = timeout

    def run(self):
        """
        Старт работы воркера
        """
        while True:
            if self.tasks_q.empty():
                break
            task = self.tasks_q.get()
            p = Process(target=task.perform)
            p.start()
            p.join(self.timeout)
            p.terminate()


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
        self.a_p = []

    def run(self):
        """
        Запускайте бычка! (с)
        """
        w = [TaskProcessor(self.tasks_queue, self.timeout) for _ in range(self.n_workers)]
        for worker in w:
            p = Process(target=worker.run)
            self.a_p.append(p)
            p.start()
        while not self.tasks_queue.empty():
            for i, p in enumerate(self.a_p):
                if not p.is_alive():
                    print('Create new process')
                    process = Process(target=w[i].run)
                    process.start()
            sleep(2)
