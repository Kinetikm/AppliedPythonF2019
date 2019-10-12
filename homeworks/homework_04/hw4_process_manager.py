# !/usr/bin/env python
# coding: utf-8


from multiprocessing import Process, Queue


class Task:
    def __init__(self, abstrack_func, *args, **kwargs):
        self.abstrack_func = abstrack_func
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        if self.abstrack_func is not None:
            print('func is not None. Perform method was executed and arguments were passed to it')
            return self.abstrack_func(*self.args, **self.kwargs)
        else:
            print('func is None. Perform method did nothing')


class TaskProcessor:

    def __init__(self, tasks_queue, timeout):
        self.tasks_queue = tasks_queue
        self.timeout = timeout

    def run(self):
        while not self.tasks_queue.empty():
            task = self.tasks_queue.get()
            proc = Process(target=task.perform)
            print("process was started")
            proc.start()
            proc.join(timeout=self.timeout)
            proc.terminate()
            print("process was terminated")


class TaskManager:

    def __init__(self, tasks_queue, n_workers, timeout):
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.processes = list()
        self.workers = list()

    def run(self):
        for i_worker in range(self.n_workers):
            self.workers.append(TaskProcessor(self.tasks_queue, self.timeout))
        for worker in self.workers:
            proc = Process(target=worker.run)
            self.processes.append(proc)
            proc.start()
        while not self.tasks_queue.empty:
            temp = 0
            for proc in self.processes:
                temp += 1
                if not proc.is_alive():
                    self.processes[temp] = Process(self.workers[temp].run)
                    self.processes[temp].start()

