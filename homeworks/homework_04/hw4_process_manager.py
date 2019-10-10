#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
import random
import time


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """

    def __init__(self, *args, **kwargs):
        self.func = args[0]
        self.args = args[1:]
        self.kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        print("Started = ", *self.args, **self.kwargs)
        tmp = random.randint(1, 10)
        print(tmp)
        time.sleep(tmp)
        self.func(*self.args, **self.kwargs)
        print("Done = ", *self.args, **self.kwargs)


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
        while not self.tasks_queue.empty():
            task = self.tasks_queue.get()
            process = Process(target=task.perform)
            process.start()
            process.join(self.timeout)
            process.terminate()
        # return process


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
        self.processes = []

    def run(self):
        """
        Запускайте бычка! (с)
        """
        for _ in range(self.n_workers):
            p = Process(target=TaskProcessor(self.tasks_queue, self.timeout).run)
            p.start()
            self.processes.append(p)

        while not self.tasks_queue.empty():
            # r = random.randint(0, self.n_workers)
            # if r == 1:
            #     self.processes[r].terminate()
            #     time.sleep(1)
            #     print("Killed worker number: ", r)
            for i in range(len(self.processes)):
                if not self.processes[i].is_alive():
                    print("New process")
                    self.processes[i] = Process(target=TaskProcessor(self.tasks_queue, self.timeout).run)
                    self.processes[i].start()


init_tasks = 15
n_workers = 5
timeout = 3
queue = Queue()

for i in range(init_tasks):
    queue.put(Task(print, i))

tasks_m = TaskManager(queue, n_workers, timeout)
tasks_m.run()
queue.close()
'''
Для теста в TaskManager раскомментировать код в функции run().
'''
