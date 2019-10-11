#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Pool, Manager
import time
import os
import copy
from queue import Empty


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, target_function, args=[], kwargs={}):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.func = target_function
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        self.func(*self.args, **self.kwargs)


class TaskProcessor(Process):
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, pid_task_start_time, queue_timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        Process.__init__(self)
        self.task_queue = tasks_queue
        self.pid_task_start_time = pid_task_start_time
        self.queue_timeout = queue_timeout

    def run(self):
        """
        Старт работы воркера
        """
        pid = os.getpid()
        print("TaskProcessor[{}] started".format(pid))
        while True:
            try:
                task = self.task_queue.get(timeout=self.queue_timeout)
            except Exception as e:
                # отправить сигнал родителю!
                print("EXCEPTION ", e)
                break
            else:
                # обязательно в таком порядке, чтобы если мы .terminate() из родителя, очередь не "разрушилась"
                task_start_time = time.time()

                self.pid_task_start_time[pid] = task_start_time
                print("{} task perform! with ARGS:{}".format(pid, task.args))
                task.perform()
                task_end_time = time.time()
                print("{} task PERFORMED! with time consumed {}".format(pid, task_end_time - task_start_time))


class TaskManager(Process):
    """
    Мастер-процесс, который управляет воркерами
    """
    def __init__(self, tasks_queue, n_workers, timeout=10, queue_timeout=100):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        :param q_timeout: таймаут в секундах, из очереди пытаемся достать элемент q_timeout секунд
        """
        Process.__init__(self)
        self.t_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.q_timeout = queue_timeout

    def run(self):
        """
        Запускайте бычка! (с)
        Мастер следит, что число воркеров всегда было равно n_workers (в случае смерти пересоздает их).
        """
        # при завершения мастер процесса, нужно чтобы все таски и воркеры тоже завершились!
        # для этого делаем демонами!
        manager = Manager()
        # pid: task_start_time
        self.pid_task_start_time = manager.dict()
        # pid: TaskProcessor
        self.workers = {}

        for _ in range(self.n_workers):
            worker = TaskProcessor(self.t_queue, self.pid_task_start_time, self.q_timeout)
            worker.daemon = True  # taska не ляжет, если она создавала процесс!!
            worker.start()
            self.workers[worker.pid] = worker

        while True:
            # restart
            self.process_restart()
            # kill
            self.kill_after_timeout()

    def process_restart(self):
        new_workers_dict = {}
        for pid, worker in self.workers.items():
            if not worker.is_alive():
                print("PID[{}] is not alive!".format(worker.pid))
                new_worker = TaskProcessor(self.t_queue, self.pid_task_start_time, self.q_timeout)
                new_worker.daemon = True
                new_worker.start()
                print("NEW WORKER CREATED WITH [{}]".format(new_worker.pid))

                new_workers_dict[new_worker.pid] = new_worker
            else:
                new_workers_dict[pid] = worker

        self.workers = new_workers_dict

    def kill_after_timeout(self):
        current_time = time.time()
        # из-за многопроцессорности ФРИЗИМ состояние дикта!
        pid_task_start_time_curr = copy.deepcopy(self.pid_task_start_time)
        for pid, task_start_time in pid_task_start_time_curr.items():
            if current_time - task_start_time > self.timeout:
                # успел закончить, но его удалили!
                timeouted_worker = self.workers.get(pid)
                if timeouted_worker:
                    # убили процесс
                    print("Killing {} worker".format(pid))
                    timeouted_worker.terminate()
                    print("Killed {} worker".format(pid))
                    # чтобы не было зомби процесса
                    timeouted_worker.join()


def targ_func(sleep_time, task_id):
    print("TASK[{}] Started".format(task_id))
    time.sleep(sleep_time)
    print("TASK[{}] Ended".format(task_id))


if __name__ == '__main__':
    manager = Manager()
    queue = manager.Queue()

    tasks = []
    for i in range(10):
        args = [1 + i, i]
        task = Task(target_function=targ_func, args=args)
        tasks.append(task)

    manager = TaskManager(queue, 2, 5, 10)
    manager.start()
    print("MANAGER started with [{}]".format(manager.pid))

    for task in tasks:
        queue.put(task)

    time.sleep(2)

    print("Killing manager!")
    manager.terminate()
    print("Manager died!")
    manager.join()
