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

    def __init__(self, tasks_queue, timeout):
        self.timeout = timeout
        self.tasks = tasks_queue
        self.proc = None

    def run(self):
        self.proc = multiprocessing.Process(target=self.work)
        self.proc.start()

    def work(self):
        while True:
            if not self.tasks.empty():
                task = self.tasks.get()
                if issubclass(task.__class__, Task):
                    process = multiprocessing.Process(target=task.perform)
                    process.start()
                    start_time = time.time()
                    while process.is_alive():
                        if time.time() - start_time > self.timeout:
                            os.system("kill -9 {}".format(process.pid))
                        time.sleep(0.5)
                    process.join()
                    process.close()
                else:
                    print("Expected Task in Queue, but received otherwise")
                    raise TypeError
            else:
                time.sleep(3)


class TaskManager:

    def __init__(self, tasks_queue, n_workers, timeout):
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout

    def run(self):
        jobs = []
        sleep_time = 1 / self.n_workers
        for _ in range(self.n_workers):
            task_proc = TaskProcessor(self.tasks_queue, self.timeout)
            jobs.append(task_proc)
            task_proc.run()

        while True:
            k = 0
            for j in range(len(jobs)):
                if not jobs[j - k].proc.is_alive():
                    del jobs[j - k]
                    k += 1
                    task_proc = TaskProcessor(self.tasks_queue, self.timeout)
                    jobs.append(task_proc)
                    task_proc.run()
            time.sleep(sleep_time)
            if self.tasks_queue.empty():
                time.sleep(3)


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
    TM = TaskManager(queue, 4, 8)
    TM.run()
'''