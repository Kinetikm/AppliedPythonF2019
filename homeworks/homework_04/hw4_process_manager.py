#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import time
import random


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, value):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.value = value

    def perform(self):
        """
        Старт выполнения задачи
        """
        tm = random.randint(1, 7)
        print(self.value, 'Working.... ', tm)
        time.sleep(tm)
        print(self.value, ' Done! tm ==', tm)
        return self.value


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
        # print('Proc')
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
        global flag
        jobs = []
        tm = []
        while not self.queue.empty() or jobs:
            print(self.queue.qsize(), len(jobs))
            if (len(jobs) < self.n_workers or self.queue.qsize() < self.n_workers) and not self.queue.empty():
                t = TaskProcessor(self.queue).run()
                jobs.append(t)
                tm.append(time.clock_gettime(time.CLOCK_REALTIME))
            print('worker - queue', self.n_workers,  self.queue.qsize())
            flag = False
            if len(jobs) == self.n_workers or self.n_workers > self.queue.qsize():
                for job in jobs:
                    job.join(timeout=0.0001)
                while len(jobs):
                    for i in range(len(jobs)):
                        # print(jobs[i])
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


begin = time.clock_gettime(time.CLOCK_REALTIME)
queue = Manager().Queue()
queue.put(Task(3))
queue.put(Task(4))
queue.put(Task(5))
queue.put(Task(6))
queue.put(Task(7))
a = TaskManager(queue, 2, 4)
a.run()
# print(time.clock_gettime(time.CLOCK_REALTIME) - begin)

# V-1
# def run(self):
#     """
#     Запускайте бычка! (с)
#     """
#     while not self.queue.empty():
#         jobs = []
#         dates = {}
#         a = self.queue.qsize()
#         if a > self.n_workers:
#             a = self.n_workers
#         for _ in range(a):
#             t = TaskProcessor(self.queue).run()
#             jobs.append(t)
#             dates.update({t: time.clock_gettime(time.CLOCK_REALTIME)})
#         print(dates)
#         for job in jobs:
#             # print(1)
#             job.join(timeout=0.0001)
#             # print(2)
#             # while job.is_alive():
#             #     if time.clock_gettime(time.CLOCK_REALTIME) - dates[job] > self.timeout:
#             #         job.kill()
#             #         print('terminated  ', job)
#     return


# V-2
# def run(self):
#     """
#     Запускайте бычка! (с)
#     """
#     jobs = []
#     dates = {}
#     while not self.queue.empty():
#         # print(self.queue.qsize(), len(jobs))
#         if len(jobs) < self.n_workers or self.queue.qsize() < self.n_workers:
#             t = TaskProcessor(self.queue).run()
#             dates.update({t: time.clock_gettime(time.CLOCK_REALTIME)})
#             jobs.append(t)
#         if len(jobs) == self.n_workers:
#             for job in jobs:
#                 # print(1)
#                 job.join(timeout=0.001)
#             while len(dates):
#                 for job, tm in dates.items():
#                     if not job.is_alive() or time.clock_gettime(time.CLOCK_REALTIME) - tm > self.timeout:
#                         job.terminate()
#                         print('terminated ', job)
#                         jobs.pop(0)
#                         dates.pop(job)
#                         break
#                 break
#             # print(2)
#             # while job.is_alive():
#             #     if time.clock_gettime(time.CLOCK_REALTIME) - dates[job] > self.timeout:
#             #         job.kill()
#             #         print('terminated  ', job)
#     return

# V-3
# def run(self):
#     """
#     Запускайте бычка! (с)
#     """
#     jobs = []
#     dates = []
#     while not self.queue.empty():
#         print(self.queue.qsize(), len(jobs))
#         if len(jobs) < self.n_workers or self.queue.qsize() < self.n_workers:
#             t = TaskProcessor(self.queue).run()
#             dates.append(t)
#             jobs.append(t)
#         if len(jobs) == self.n_workers:
#             for job in jobs:
#                 # print(1)
#                 job.join(timeout=0.001)
#             while len(dates):
#                 if not dates[0].is_alive():
#                     jobs.pop(0)
#                     dates.pop(0)
#                     break
#                 if not dates[1].is_alive():
#                     jobs.pop(1)
#                     dates.pop(1)
#                     break
#             # print(2)
#             # while job.is_alive():
#             #     if time.clock_gettime(time.CLOCK_REALTIME) - dates[job] > self.timeout:
#             #         job.kill()
#             #         print('terminated  ', job)
#     return

# V-4 - worked version with timer
# def run(self):
#     """
#     Запускайте бычка! (с)
#     """
#     jobs = []
#     dates = []
#     tm = []
#     while not self.queue.empty():
#         print(self.queue.qsize(), len(jobs))
#         if len(jobs) < self.n_workers or self.queue.qsize() < self.n_workers:
#             t = TaskProcessor(self.queue).run()
#             dates.append(t)
#             jobs.append(t)
#             tm.append(time.clock_gettime(time.CLOCK_REALTIME))
#         print('worker - queue', self.n_workers, self.queue.qsize())
#         if len(jobs) == self.n_workers or self.n_workers > self.queue.qsize():
#             for job in jobs:
#                 job.join(timeout=0.0001)
#             while len(dates):
#                 if not dates[0].is_alive() or time.clock_gettime(time.CLOCK_REALTIME) - tm[0] > self.timeout:
#                     print('time == ', time.clock_gettime(time.CLOCK_REALTIME) - tm[0])
#                     if dates[0].is_alive():
#                         dates[0].terminate()
#                         print('terminated ', dates[0])
#                     jobs.pop(0)
#                     tm.pop(0)
#                     dates.pop(0)
#                     break
#                 if not dates[1].is_alive() or time.clock_gettime(time.CLOCK_REALTIME) - tm[1] > self.timeout:
#                     print('time == ', time.clock_gettime(time.CLOCK_REALTIME) - tm[1])
#                     if dates[1].is_alive():
#                         dates[1].terminate()
#                         print('terminated ', dates[1])
#                     jobs.pop(1)
#                     tm.pop(1)
#                     dates.pop(1)
#                     break
