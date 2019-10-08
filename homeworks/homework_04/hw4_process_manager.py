#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import time
import random


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, value):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.value = value

    def perform(self):
        """
        Старт выполнения задачи
        """
        print(self.value)
        tm = random.randint(1, 5)
        time.sleep(tm)
        print(self.value, ' slept ', tm, 'secs')
        return self.value


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.task = tasks_queue
        self.start = time.process_time()

    def run(self):
        """
        Старт работы воркера
        """
        hm = Process(target=self.task.get().perform)
        hm.start()
        return hm


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
        while not self.queue.empty():
            jobs = []
            a = self.queue.qsize()
            if a > self.n_workers:
                a = self.n_workers
            for _ in range(a):
                t = TaskProcessor(self.queue).run()
                jobs.append(t)
            for job in jobs:
                # if time.clock() - job.start > self.timeout:
                #     job.terminate()
                job.join()
        return

    # def killer(self, queue):
    #     while 1:
    #         if queue.empty():
    #             break
    #         # for


# print(time.clock_gettime(time.CLOCK_REALTIME))
# queue = Manager().Queue()
# queue.put(Task('hello'))
# queue.put(Task('my'))
# queue.put(Task('name'))
# queue.put(Task('is'))
# queue.put(Task('Alex'))
# a = TaskManager(queue, 2, 3)
# a.run()
# print(time.clock_gettime(time.CLOCK_REALTIME))
