#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import os
from time import time
from simple_task import simple_task  # для тестирования


class Task:

    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        return self.function(*self.args, **self.kwargs)


class TaskProcessor:

    def __init__(self, tasks_queue, timeout):
        self.tasks = tasks_queue
        self.timeout = timeout
        self.run()

    def run(self):
        while True:
            if not self.tasks.empty():
                task = self.tasks.get()
                proc = Process(target=task.perform)
                proc.start()
                start_time = time()
                while True:
                    if proc.is_alive():
                        if time() - start_time >= self.timeout:
                            proc.terminate()
                            print('Задача прервана')
                    else:
                        break
                proc.join()


class TaskManager:

    def __init__(self, tasks_queue, n_workers, timeout):
        self.tasks = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout

    def run(self):
        processes = []
        for _ in range(self.n_workers):
            process = Process(target=TaskProcessor, args=(self.tasks, self.timeout))
            processes.append(process)
            process.start()

        # добавляем задачу

        for i in processes:
            i.join()


# запуск
if __name__ == '__main__':
    tasks_queue = Manager().Queue()
    a = Task(simple_task, 2, 5, arg1=6, arg2=7)
    b = Task(simple_task, 3, 5, arg1=6, arg2=8)
    c = Task(simple_task, 4, 5, arg1=6, arg2=9)
    d = Task(simple_task, 5, 5, arg1=6, arg2=10)
    e = Task(simple_task, 6, 5, arg1=6, arg2=11)
    f = Task(simple_task, 7, 5, arg1=6, arg2=12)
    for task in (a, b, c, d, e, f):
        tasks_queue.put(task)
    task_manager = TaskManager(tasks_queue, 1, 5)
    task_manager.run()
