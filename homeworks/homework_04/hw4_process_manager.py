#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Queue
from time import time, sleep
import signal
from contextlib import contextmanager


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.setitimer(signal.ITIMER_REAL, seconds, 0)
    try:
        yield
    finally:
        signal.alarm(0)


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
    def __init__(self, tasks_queue, res_queue, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        super().__init__()
        self.tasks_queue = tasks_queue
        self.res_queue = res_queue
        self.timeout = timeout

    def run(self):
        """
        Старт работы воркера
        """

        item = self.tasks_queue.get()
        if self.timeout is not None:
            try:
                with time_limit(self.timeout):
                    res = item.perform()
            except TimeoutException:
                res = 'Timed out!'
        else:
            res = item.perform()

        if res is None:
            self.res_queue.put('Function does not return anything!')
        elif res == 'Timed out!':
            self.res_queue.put('Function`s performance was not end')
        else:
            self.res_queue.put(res)


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

        while True:
            while len(jobs) < self.n_workers:
                job = TaskProcessor(self.tasks_queue, self.res_queue, self.timeout)
                jobs.append(job)
                job.start()

            for i, job in enumerate(jobs):
                if not job.is_alive():
                    del jobs[i]


# Первый аргумент - время сна, остальное по желанию

def func(*args, **kwargs):
    s = 0
    sleep(args[0])
    for arg in args:
        s += arg
    print(f'What a wonderful homework! I will sleep for {args[0]} second(s)')
    for kw in kwargs.values():
        s += kw
    return s


n_workers = 2
time_out = 3.1
queue_0 = Manager().Queue()
queue_1 = Manager().Queue()
a = TaskManager(queue_0, queue_1, n_workers, time_out)
a.start()

queue_0.put(Task(func, 1, 7))
queue_0.put(Task(func, 1, 7, 0.5, c=2))
queue_0.put(Task(func, 1, 7, 0.5, c=2))
queue_0.put(Task(func, 1, 7, 0.5, c=2))
queue_0.put(Task(func, 1, 7, c=2, d=3))
queue_0.put(Task(func, 5, 7, c=2, d=4))
queue_0.put(Task(func, 3, 7, c=2.3, d=4))


while True:
    while queue_1.qsize():
        print(queue_1.get())
