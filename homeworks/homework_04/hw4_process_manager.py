import multiprocessing
import time
import os
from abc import ABC, abstractmethod
from multiprocessing import Manager


class Task(ABC):

    @abstractmethod
    def perform(self):
        pass


class TaskProcessor:

    def __init__(self, tasks_queue):
        self.task = tasks_queue.get()
        self.start_time = None
        self.proc = None

    def run(self):
        self.proc = multiprocessing.Process(target=self.task.perform)
        self.proc.start()
        self.start_time = time.time()


class TaskManager:

    def __init__(self, tasks_queue, n_workers, timeout):
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout

    def run(self):
        jobs = []
        sleep_time = 1 / self.n_workers
        if self.tasks_queue.qsize() < self.n_workers:
            self.n_workers = self.tasks_queue.qsize()
        for _ in range(self.n_workers):
            task_proc = TaskProcessor(self.tasks_queue)
            jobs.append(task_proc)
            task_proc.run()
        while not self.tasks_queue.empty():
            k = 0
            for j in range(len(jobs)):
                if jobs[j - k].proc.is_alive():
                    if time.time() - jobs[j - k].start_time > self.timeout:
                        os.system("kill -9 {}".format(jobs[j - k].proc.pid))
                        print("Time exceeded for Queue[{}]".format(jobs[j - k].task.size), ". Process was killed")
                        del jobs[j - k]
                        k += 1
                        if not self.tasks_queue.empty():
                            task_proc = TaskProcessor(self.tasks_queue)
                            jobs.append(task_proc)
                            task_proc.run()
                else:
                    del jobs[j - k]
                    k += 1
                    if not self.tasks_queue.empty():
                        task_proc = TaskProcessor(self.tasks_queue)
                        jobs.append(task_proc)
                        task_proc.run()
            time.sleep(sleep_time)

        while len(jobs) != 0:
            k = 0
            for j in range(len(jobs)):
                if jobs[j - k].proc.is_alive():
                    if time.time() - jobs[j - k].start_time > self.timeout:
                        print("Time exceeded for Queue[{}]".format(jobs[j - k].task.size), ". Process was killed")
                        os.system("kill -9 {}".format(jobs[j - k].proc.pid))
                        del jobs[j - k]
                        k += 1
                else:
                    del jobs[j - k]
                    k += 1
                time.sleep(sleep_time)


# Для проверки:
'''
class TaskExample(Task):
    def __init__(self, size):
        self.size = size

    def perform(self):
        print(str(self.size) + " started")
        time.sleep(self.size % 10)


if __name__ == '__main__':
    manager = Manager()
    queue = manager.Queue()
    for i in range(50):
        queue.put(TaskExample(i))
    TM = TaskManager(queue, 4, 7)
    TM.run()
'''