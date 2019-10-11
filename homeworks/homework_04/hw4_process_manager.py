#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import time

class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, func, *args):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.func = func
        self.args = args

    def perform(self):
        """
        Старт выполнения задачи
        """
        if not self.args:
            res = self.func()
        else:
            res = self.func(*self.args)
        return res


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        self.task = tasks_queue.get()
        self.time0 = None
        self.proc = None

    def run(self):
        self.proc = Process(target=self.task.perform)
        self.proc.start()
        self.time0 = time.time()


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
        self.tasks_q = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.workers = []
        print("here")


    def run(self):
        if self.tasks_q.qsize() < self.n_workers:
            self.n_workers = self.tasks_q.qsize()
        for i in range(self.n_workers):
            # print("task create0 i = ", i)
            task_proc = TaskProcessor(self.tasks_q)
            self.workers.append(task_proc)
            task_proc.run()
        while len(self.workers) != 0:
            for task in self.workers:
                # print("workers len = ", len(self.workers))
                if task.proc.is_alive():
                    # print("proc alive")
                    if time.time() - task.time0 < self.timeout:
                        continue
                # else:
                    # print("proc Dead")
                task.proc.terminate()
                print('Process terminated')
                self.workers.remove(task)
                if not self.tasks_q.empty():
                    task_proc = TaskProcessor(self.tasks_q)
                    self.workers.append(task_proc)
                    task_proc.run()
            time.sleep(1 / self.n_workers)

# TESTIN'
'''
def sleep(num):
        print(str(num) + " started")
        time.sleep(num % 10)
print("START SLEEPIN'")
manager = Manager()
queue = manager.Queue()
for i in range(10):
    queue.put(Task(sleep,i))
tm = TaskManager(queue, 4, 7)
tm.run()
'''
