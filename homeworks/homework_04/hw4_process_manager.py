#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import time


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """

    def __init__(self, func, *args, **kwargs):
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
        self.tasks_queue = tasks_queue
        self.proc = None
        self.start_time = 0

    def run(self):
        """
        Старт работы воркера
        """
        task = self.tasks_queue.get()
        self.proc = Process(target=task.perform, args=())
        self.proc.start()
        self.start_time = time.time()

    def stop(self):
        self.proc.terminate()


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
        self.queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout

    def run(self):
        """
        Запускайте бычка! (с)
        """
        workers = []
        last_start = time.time()
        while time.time() - last_start < 4*self.timeout:
            for worker in workers:
                if worker.proc.is_alive() and (time.time() - worker.start_time < self.timeout):
                    continue
                worker.stop()
                workers.remove(worker)
            if (len(workers) < self.n_workers) and (self.queue.qsize() > 0):
                for i in range(min(self.n_workers - len(workers), self.queue.qsize())):
                    t_proc = TaskProcessor(self.queue)
                    t_proc.run()
                    last_start = t_proc.start_time
                    workers.append(t_proc)
#
#
# def f(x):
#     time.sleep(x % 5)
#     print(x)
#
#
# if __name__ == "__main__":
#     mq = Manager().Queue()
#     for i in range(20):
#         mq.put(Task(f, i))
#     tm = TaskManager(mq, 5, 2)
#     tm.run()
#     Вывело 0, 5, 1, 6, 10, 11, 15, 16
