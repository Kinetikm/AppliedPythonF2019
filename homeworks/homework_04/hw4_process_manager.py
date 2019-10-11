#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
import time


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        self.function(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, timeout, num):
        self.tasks = tasks_queue
        self.timeout = timeout
        self.num = num

    def run(self):
        while not self.tasks.empty():
            task = self.tasks.get()
            print(self.num, task.args, task.kwargs)
            process = Process(target=task.perform, args=())
            process.start()
            process.join(timeout=self.timeout)
            # try:
            #     process.join(timeout=self.timeout)
            # except TimeoutError:
            #     process.terminate()
            #     print('Task was terminated')


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
        self.tasks = tasks_queue
        self.max_number_workers = n_workers
        self.timeout = timeout
        self.workers = [] * self.max_number_workers
        self.work_procs = [] * self.max_number_workers
        self.alive_workers = 0

    def check_workers(self):
        if self.alive_workers == 0:
            return
        for index, worker in enumerate(self.work_procs):
            if not worker.is_alive():
                self.work_procs.pop(index)
                self.workers.pop(index)
                self.alive_workers -= 1

    def run(self):
        """
        Запускайте бычка! (с)
        """
        n=0
        while not self.tasks.empty():
            self.check_workers()
            while self.alive_workers != self.max_number_workers:
                worker = TaskProcessor(self.tasks, self.timeout, n)
                n+=1
                self.workers.append(worker)
                process = Process(target=worker.run, args=())
                process.start()
                self.work_procs.append(process)


def func(timeout=1, text="default"):
    time.sleep(timeout)
    print(text)


q = Queue()

for i in range(15):
    task = Task(func, *(i,), **{"text": f"task number {i}"})
    q.put(task)

manager = TaskManager(q, 5, 7)
manager.run()