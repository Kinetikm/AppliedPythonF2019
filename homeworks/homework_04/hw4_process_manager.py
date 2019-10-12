from multiprocessing import Process, Manager
from time import time


class Result:
    def __init__(self, func, args, kwargs, result):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = result


class Task:
    def __init__(self, func, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.func = func

    def perform(self, result_list):
        result_list.append(Result(self.func, self.args, self.kwargs,
                                  self.func(*self.args, **self.kwargs)))


class TaskProcessor:
    def __init__(self, tasks_queue):
        self.tasks_queue = tasks_queue

    def run(self, result_list):
        task = self.tasks_queue.get()
        job = Process(target=task.perform, args=(result_list,))
        job.start()
        return (job, time())


class TaskManager:

    def __init__(self, tasks_queue, n_workers, timeout):
        self.task_processor = TaskProcessor(tasks_queue)
        self.n_workers = n_workers
        self.timeout = timeout

    def run(self):
        jobs = []
        result_list = Manager().list()
        while self.task_processor.tasks_queue.qsize() != 0:
            if len(jobs) < self.n_workers:
                jobs.append(self.task_processor.run(result_list))
            else:
                while True:
                    if self.check_jobs(jobs):
                        break
        while len(jobs) != 0:
            self.check_jobs(jobs)

    def check_jobs(self, jobs):
        for i in range(len(jobs)):
            job, t = jobs[i]
            if not job.is_alive():
                jobs.pop(i)
                return True
            if time() - t > self.timeout:
                job.kill()
                jobs.pop(i)
                return True
        return False
