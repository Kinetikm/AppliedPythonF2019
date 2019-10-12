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
        self.ret = None

    def perform(self):
        """
        Старт выполнения задачи
        """
        self.ret = self.func(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, num):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.queue = tasks_queue
        self.num = num

    def run(self, dct):
        """
        Старт работы воркера
        """
        while True:
            item = self.queue.get()
            dct[self.num] = time.time()
            if item == 'kill':
                raise SystemExit
            elif True:
                try:
                    item.perform()
                except Exception:
                    item.ret = "Execution Error"
                self.queue.put((item.ret,dct[self.num]))


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
        self.queue = tasks_queue
        self.num_workers = n_workers
        self.timeout = timeout
        for i in range(self.num_workers):
            self.queue.put('kill')

    def run(self):
        """
        Запускайте бычка! (с)
        """
        procs = Manager().dict()
        proc = Process(target=self.control, args=(procs,))
        proc.start()
        proc.join()
        lst = []
        for i in range(self.queue.qsize()):
            lst.append(self.queue.get())
        return [i[0] for i in sorted(lst, key=lambda a: a[1])]

    def control(self, procs):
        pr = []
        workers = [TaskProcessor(self.queue, i) for i in range(self.num_workers)]
        for i in range(self.num_workers):
            proc = Process(target=workers[i].run, args=(procs,))
            procs[i] = 0
            pr.append(proc)
            proc.start()
        time.sleep(self.timeout)
        while True:
            for i in range(len(procs)):
                if time.time() - procs[i] > self.timeout:
                    pr[i].kill()
                    pr[i].join()
                    self.queue.put(('Timeout Error',procs[i]))
                    pr[i] = Process(target=workers[i].run, args=(procs,))
                    procs[i] = time.time()
                    pr[i].start()
            if all([not i.is_alive() for i in pr]):
                break
        for i in pr:
            i.join()


def f(n, t):
    time.sleep(6-t)
    return 1/n
lst = [Task(f, i, i) for i in range(6)]
q = Manager().Queue()
for i in lst:
    q.put(i)
a = TaskManager(q, 3, 5)
print(a.run())
