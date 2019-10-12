#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process


class Task:

    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        self.function(*self.args, **self.kwargs)


class TaskProcessor:

    def __init__(self, tasks_queue):
        self.tasks_queue = tasks_queue
        self.time = None

    def run(self):
        while True:
            if self.tasks_queue.empty():
                break
            task = self.tasks_queue.get()
            process = Process(target=task.perform())
            process.start()
            self.time = time.time()
            process.terminate()



class TaskManager:

    def __init__(self, tasks_queue, n_workers, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.alive_worker = []

    def run(self):

        flag = self.tasks_queue.empty()
        tasks = [TaskProcessor(self.tasks_queue) for i in range(n_workers)]
        for task in tasks:
            process = Process(target=task.run())
            self.alive_worker.append(process)
            process.start()
        while flag is not True:
            index = 0
            for task in self.alive_worker:
                if time.time() - self.alive_worker[index].time > self.timeout:
                    alive_worker[index].process.terminate()
                    alive_worker[index].process.join()
                    task.append(tasks)
                    index = 0
                if not self.alive_worker[index].is_alive():
                    process = Process(target=tasks[index].run())
                    process.start()
            flag = self.tasks_queue.empty()
