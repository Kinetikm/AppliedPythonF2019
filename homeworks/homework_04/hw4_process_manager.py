#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import time
import random
import urllib.request


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """

    def __init__(self):
        """
        Пофантазируйте, как лучше инициализировать
        """

    def perform(self):
        """
        Старт выполнения задачи
        """
        pass


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.task = tasks_queue
        self.start = time.clock_gettime(time.CLOCK_REALTIME)

    def run(self):
        """
        Старт работы воркера
        """
        hm = Process(target=self.task.get().perform)
        hm.start()
        return hm


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
        self.n_workers = n_workers
        self.timeout = timeout
        self.worker_queue = Manager().Queue()

    def run(self):
        """
        Запускайте бычка! (с)
        """
        flag = False
        jobs = []
        tm = []
        while not self.queue.empty() or jobs:
            print(self.queue.qsize(), len(jobs))
            if (len(jobs) < self.n_workers or self.queue.qsize() < self.n_workers) and not self.queue.empty():
                t = TaskProcessor(self.queue).run()
                jobs.append(t)
                tm.append(time.clock_gettime(time.CLOCK_REALTIME))
            print('worker - queue', self.n_workers, self.queue.qsize())
            if len(jobs) == self.n_workers or self.n_workers > self.queue.qsize():
                for job in jobs:
                    job.join(timeout=0.0001)
                while len(jobs):
                    for i in range(len(jobs)):
                        if not jobs[i].is_alive() or time.clock_gettime(time.CLOCK_REALTIME) - tm[i] > self.timeout:
                            print('time == ', time.clock_gettime(time.CLOCK_REALTIME) - tm[i])
                            if jobs[i].is_alive():
                                jobs[i].terminate()
                                print('terminated ', jobs[i])
                            jobs.pop(i)
                            tm.pop(i)
                            flag = True
                            break
                    if flag:
                        flag = False
                        break
        return


# An example of usage is below... Also uncomment import libraries

class Mult(Task):
    def __init__(self, f, argument):
        super().__init__()
        self.ar = argument
        self.f = f

    def perform(self):
        tm = random.randint(1, 7)
        print(self.ar, 'Working.... ', tm)
        time.sleep(tm)
        print(self.ar, ' Done! tm ==', tm)
        return self.f(self.ar)


def add(values):
    return sum(values)


class EasyTask(Task):
    def __init__(self, argument):
        super().__init__()
        self.ar = argument

    def perform(self):
        tm = random.randint(1, 7)
        print(self.ar, 'Working.... ', tm)
        time.sleep(tm)
        print(self.ar, ' Done! tm ==', tm)
        return self.ar


class DownloadData(Task):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def perform(self):
        tm = random.randint(1, 7)
        print(self.url, 'Working.... ', tm)
        time.sleep(tm)
        print(self.url, ' Done! tm ==', tm)
        response = urllib.request.urlopen(self.url)
        data = response.read()
        text = data.decode('utf-8')
        print('result ===', text)
        return text


begin = time.clock_gettime(time.CLOCK_REALTIME)
queue = Manager().Queue()
queue.put(Mult(add, [5, 7, 1]))
queue.put(EasyTask(3 * 5))
queue.put(EasyTask('agagag'))
queue.put(EasyTask([2, 5, 6]))
queue.put(EasyTask({3: 44}))
queue.put(EasyTask(None))
queue.put(DownloadData('https://habr.com/ru/company/otus/blog/458694/'))
a = TaskManager(tasks_queue=queue, n_workers=2, timeout=5)
a.run()
