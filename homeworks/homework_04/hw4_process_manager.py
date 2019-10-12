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
    def __init__(self, func, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        self.func(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue
        self.pr = None
        self.time = None

    def run(self):
        """
        Старт работы воркера
        """
        if not self.tasks_queue.empty():
            task = self.tasks_queue.get()
            if not isinstance(task, Task):
                raise TypeError("Expected Task, found something else")
            else:
                self.pr = Process(target=task.perform)

                self.pr.start()
                print("Process with id = {} has started".format(self.pr.pid))
                self.time = time.time()

    def kill(self):
        print("Process with id = {} was killed".format(self.pr.pid))
        self.pr.terminate()
        self.pr.join()


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
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.period = 0.1 * self.timeout / self.n_workers

    def run(self):
        """
        Запускайте бычка! (с)
        """
        if self.n_workers < self.tasks_queue.qsize():
            workers = [TaskProcessor(tasks_queue=self.tasks_queue) for i in range(self.n_workers)]
        else:
            workers = [TaskProcessor(tasks_queue=self.tasks_queue) for i in range(self.tasks_queue.qsize())]
        for worker in workers:
            worker.run()
        while not self.tasks_queue.empty():
            for i in range(len(workers)):
                if workers[i].pr is None:
                    del workers[i]
                    continue
                if not workers[i].pr.is_alive():
                    print("Process with id = {} done!".format(workers[i].pr.pid))
                    workers[i].pr.join()
                    del workers[i]
                    workers.append(TaskProcessor(self.tasks_queue))
                    workers[-1].run()
                elif time.time() - workers[i].time > self.timeout:
                    workers[i].kill()
                    del workers[i]
                    workers.append(TaskProcessor(self.tasks_queue))
                    workers[-1].run()
            time.sleep(self.period)
        while len(workers) != 0:
            i = 0
            while i < len(workers):
                if not workers[i].pr.is_alive():
                    print("Process with id = {} done!".format(workers[i].pr.pid))
                    del workers[i]
                elif time.time() - workers[i].time > self.timeout:
                    workers[i].kill()
                    del workers[i]
                i += 1
            time.sleep(self.period)

'''
def cat():
    print("я упал")
    time.sleep(2)  # (полежал)
    print("я встал")


def doubler(a):
    time.sleep(1)
    print("I have doubled {}!".format(a))
    return 2 * a


manager = Manager()
queue = manager.Queue()
queue.put(Task(cat))
queue.put(Task(doubler, 4))
queue.put(Task(doubler, 3))
queue.put(Task(cat))
TM = TaskManager(queue, 3, 3)
TM.run()
'''
