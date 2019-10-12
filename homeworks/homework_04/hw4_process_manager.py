#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue, current_process
import time
from random import randint


class Task:
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        self.function(*self.args, **self.kwargs)


class TaskProcessor:
    def __init__(self, tasks_queue, timeout):
        self.tasks = tasks_queue
        self.timeout = timeout

    def run(self):
        print("** process {} start".format(current_process().name))
        while not self.tasks.empty():
            task = self.tasks.get()
            process = Process(target=task.perform, args=())
            process.start()
            process.join(timeout=self.timeout)
            if process.exitcode is None:
                process.terminate()


class TaskManager:
    def __init__(self, tasks_queue, n_workers, timeout):
        self.tasks = tasks_queue
        self.amount = n_workers
        self.timeout = timeout
        self.procs = [Process() for _ in range(n_workers)]

    def run(self):
        while not self.tasks.empty():
            i = 0
            while i < len(self.procs):
                if not self.procs[i].is_alive():
                    task = TaskProcessor(self.tasks, self.timeout)
                    self.procs[i] = Process(target=task.run, args=())
                    self.procs[i].start()
                i += 1

# ---------------------TEST--------------------------
            if randint(0, 9) < 1:
                ind = randint(0, len(self.procs)-1)
                print("kill {}".format(self.procs[ind].name))
                self.procs[ind].terminate()


def foo(timeout, txt):
    time.sleep(timeout)
    print(txt)


q = Queue()

for i in range(50):
    task = Task(foo, *(i, "-- task {}".format(i)))
    q.put(task)

manager = TaskManager(q, 15, 10)
manager.run()