#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process
import time


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, func, ret, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать

        """
        self._func = func
        self._args = args or None
        self._kwargs = kwargs or None

    def perform(self):
        """
        Старт выполнения задачи
        """
        if args is not None:
            if kwargs is not None:
                return self._func(self._args, self._kwargs)
            else:
                return self._func(self._args)
        else:
            return self._func()


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self._task = tasks_queue.get()
        self.busy = False
        self._in_process = None  # процесс, который запускает непосредственно воркер

    def run(self):
        """
        Старт работы воркера
        """
        self.busy = True
        self._in_process = Process(target=self._task.perform())
        self._in_process.start()
        self._in_process.join()
        self.busy = False

    def terminate(self, tasks_queue=None):
        self._in_process.terminate()
        self.busy = False
        if tasks_queue is not None:
            self._task = tasks_queue.get()
            self.run()

    def wake(self, tasks_queue):
        self._task = tasks_queue.get()
        self.run()


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
        self._tasks_queue = tasks_queue
        self._n_workers = n_workers
        self._timeout = timeout

    def run(self):
        """
        Запускайте бычка! (с)
        """
        # список состояний воркеров [id, worker, start_time]
        workers = ([i, None, None] for i in range(self._n_workers))
        while workers:
            for worker in workers:
                if worker[1] is None:  # если воркер не инициализирован
                    worker[1] = TaskProcessor(self._tasks_queue)
                    worker[1].run()
                    worker[2] = time.clock()
                elif not worker[1].busy:  # если воркер ничем не занят
                    if not self._tasks_queue.empty():
                        worker[1].wake(tasks_queue)
                        worker[2] = time.clock()
                    else:
                        workers.remove(worker)
                elif time.clock() - worker[2] > self._timeout:  # если воркер залип
                    if self._tasks_queue.empty():
                        worker[1].terminate()
                        workers.remove(worker)
                    else:
                        worker[1].terminate(self._tasks_queue)
                        worker[2] = time.clock()
