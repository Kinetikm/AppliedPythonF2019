#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
from random import randint
from time import time, sleep


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """

    def __init__(self, func, *args):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.f = func
        self.args = args

    def perform(self):
        """
        Старт выполнения задачи
        """
        if len(self.args) == 0:
            self.f()
        elif len(self.args) == 1:
            self.f(self.args[0])
        else:
            self.f(self.args)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue, timeout, i=0):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param i: номер воркера для наглядности работы
        """
        self.i = i
        self.process = None
        self.timeout = timeout
        self.tasks_q = tasks_queue

    def run(self):
        while not self.tasks_q.empty():
            task = self.tasks_q.get()
            print(self.i, "start")
            self.process = Process(target=task.perform)
            self.process.start()
            self.process.join(timeout=self.timeout)
            self.process.terminate()
            print(self.i, "end")


class TaskManager:
    def __init__(self, tasks_queue, n_workers, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """
        self.queue = tasks_queue
        self.timeout = timeout
        self.count = n_workers
        self.processor = []
        self.workers = [TaskProcessor(self.queue, timeout, i) for i in range(n_workers)]

    def run(self):
        """
        Запускайте бычка! (с)
        """
        for worker in self.workers:
            proc = Process(target=worker.run)
            self.processor.append(proc)
            proc.start()

        f = True                                                                    # it`
        time_s = time()                                                             # s
        while not self.queue.empty():
            if f and time() - time_s > 4:                                           # for
                self.processor[randint(0, len(self.processor) - 1)].terminate()     # test`
                f = False                                                           # s
            for i, proc in enumerate(self.processor):
                if not proc.is_alive():
                    proc.terminate()
                    self.workers[i] = TaskProcessor(self.queue, self.timeout, -1)
                    self.processor[i] = Process(target=self.workers[i].run)
                    self.processor[i].start()


def for_test(q):
    def add_in_queue(q):
        sleep(5)
        time_s = time()
        while time() - time_s < 20:
            sleep(randint(1, 3))
            print("put in queue")
            q.put(Task(sleep, randint(1, 3)))

    add = Process(target=add_in_queue, args=(q,))
    add.start()


queue = Queue()
for _ in range(50):
    queue.put(Task(sleep, randint(1, 3)))

for_test(queue)

tm = TaskManager(queue, 3, 10)
tm.run()

queue.close()
queue.join_thread()
