#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager,
from queue import Queue
import time


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """

    def __init__(self, funk, args=[], kwrds={}):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.funk = funk
        self.args = args
        self.kwrds = kwrds

    def perform(self):
        """
        Старт выполнения задачи
        """
        print("Таск в работе")
        return self.funk(*self.args, **self.kwrds)


class TaskProcessor(Process):
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue, initial, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """

        super().__init__()
        self.task_queue = tasks_queue
        self.initial_time = initial
        self.tomeout = timeout

    def run(self):
        """
        Старт работы воркера
        """
        while not self.task_queue.empty():
            task = self.task_queue.get()
            print("Новый таск взять в работу")
            task.perform()
            print("Таск завершён")


class TaskManager(Process):
    """
    Мастер-процесс, который управляет воркерами
    """

    def __init__(self, tasks_queue: Queue, n_workers, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """

        super().__init__()
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.worker_list = {}
        self.pid_list = []

    def timeout_killer(self, pid):
        # true - no timeout
        now = time.time()
        pid_init = self.worker_list[pid].initial_time
        timeoutr = self.timeout
        if now - pid_init > timeoutr:
            print("Убивание {} воркера".format(pid))
            self.worker_list[pid].terminate()
            print("Убит {} воркер".format(pid))
            # чтобы не было зомби процесса
            self.worker_list[pid].join()
            self.worker_list.pop(pid)
            self.pid_list.remove(pid)
            return False
        return True

    def recreate(self, worker_dict):
        temp_worker_dict = {}
        temp_pid_list = []
        for pid in self.pid_list:
            if self.timeout_killer(pid):
                if not worker_dict[pid].is_alive():
                    worker = TaskProcessor(self.tasks_queue, self.worker_list[pid].initial_time, self.timeout)
                    worker.daemon = True
                    worker.start()
                    print("пересоздали ", worker.pid, " воркера, который был ", pid)
                    temp_worker_dict[worker.pid] = worker
                    temp_pid_list.append(worker.pid)
                else:
                    temp_worker_dict[pid] = worker_dict[pid]
                    temp_pid_list.append(pid)

        self.worker_list = temp_worker_dict
        self.pid_list = temp_pid_list

    def run(self):
        """
        Запускайте бычка! (с)
        """

        for workers_num in range(self.n_workers):
            print("запускаю новый воркер")
            worker = TaskProcessor(self.tasks_queue, time.time(), self.timeout)
            worker.daemon = True
            worker.start()
            self.worker_list[worker.pid] = worker
            self.pid_list.append(worker.pid)
            print("запустил новый воркер", worker.pid)

        while True:
            self.recreate(self.worker_list)


def printer(number, task_id):
    print("TASK[{}] Started".format(task_id))
    print("THIS TASK SAYYYYY: ", number)
    time.sleep(1)
    print("TASK[{}] Ended".format(task_id))


if __name__ == '__main__':
    manager = Manager()
    queue = manager.Queue()

    tasks = []
    for i in range(10):
        args = [1 + i, i]
        task = Task(funk=printer, args=args)
        tasks.append(task)

    manager = TaskManager(queue, 2, 2)
    manager.start()
    print("Менеджер рождён и наречен быть [{}]".format(manager.pid))

    for task in tasks:
        queue.put(task)

    time.sleep(5)

    print("Инициализация убийства менеджера!")
    manager.terminate()
    print("Кирдык менеджеру!")
    manager.join()
