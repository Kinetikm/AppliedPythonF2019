#!/usr/bin/env python
# coding: utf-8
# README!!!!!!!!!!!!!
# Объясняю решения, которые в данной работе предпринял и логику:
#
# 1. Тот, кто запускает, создает процесс TaskManager, а также Pipe, для общения с мэнеджером
# Это нужно потому, что у нас используется очередь, и если вдруг мастер процесс вызовет manager.terminate(), он
# начнет высвобождать ресурсы и повредит очередь, которая по условию обязана быть. Очередь будет недоступна для детей.
# Мэнеджер слушает pipe conn, и как только там что-то появляется, убивает всех детей и завершает беск цикл.
# Делать .terminate() можно, в данном случае, очередь повредится и при попытке достать из нее что-либо выбросит исключения
# (у меня были EOFError и Broken Pipe Error).
# Поэтому в процессах у меня стоит обработчик с Exception(читайте п.2)
#
# 2. Если очередь имеет переменный размер(может как уменьшаться так и увеличиваться), то тогда нельзя использовать queue.size()
# или queue.empty(), согласно документации эти методы ненадежны в многопроцессорном режиме.
# По этой причине я использую q_get_timeout, по истечению которого выбрасывается исключение (queue.get(timeout=)), что является
# индикатором того, что в очереди больше ничего нет и тогда я записываю в "shared список" pid этого процесса.
# Если так получилось, что все воркеры сообщили о том, что очередь пуста, тогда мэнеджер убивает все процессы и завершает работу.

from multiprocessing import Process, Pool, Manager, Queue, Pipe, active_children
import time
import os
import copy


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
    def __init__(self, tasks_queue, pid_task_start_time, q_get_timeout, q_timeouted):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param pid_task_start_time: словарь, хранящий pid и время, когда таска началась
        :param q_get_timeout: время, в течение которого процесс пытается достать из очереди таску
        :param q_timeouted: список из pidов, которые не смогли достать из очереди в течение q_get_timeout
        """
        Process.__init__(self)
        self.task_queue = tasks_queue
        self.pid_task_start_time = pid_task_start_time
        self.q_get_timeout = q_get_timeout
        self.q_timeouted = q_timeouted

    def run(self):
        """
        Старт работы воркера
        """
        pid = os.getpid()
        # print("TaskProcessor[{}] started".format(pid))
        while True:
            try:
                task = self.task_queue.get(timeout=self.q_get_timeout)
            except Exception:
                self.q_timeouted.append(pid)
                return
            else:
                if not isinstance(task, Task):
                    return

                task_start_time = time.time()

                self.pid_task_start_time[pid] = task_start_time
                # print("{} TASK[{}] perform!".format(pid, task.args[1]))
                task.perform()
                # task_end_time = time.time()
                # print("{} task PERFORMED! with time consumed {}".format(pid, task_end_time - task_start_time))


class TaskManager(Process):

    def __init__(self, tasks_queue, n_workers, conn, timeout=10, q_get_timeout=100):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        :param q_get_timeout: таймаут в секундах, из очереди пытаемся достать элемент q_timeout секунд
        :param main_conn: соединение с вызывающим процессом(Pipe)
        """
        Process.__init__(self)
        self.t_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.q_get_timeout = q_get_timeout
        self.main_conn = conn

    def run(self):
        manager = Manager()
        # pid: task_start_time
        self.pid_task_start_time = manager.dict()
        # pid after q_get_timeout
        self.q_timeouted = manager.list()
        # pid: TaskProcessor
        self.workers = {}

        for _ in range(self.n_workers):
            worker = self.make_worker()
            worker.start()
            self.workers[worker.pid] = worker

        while True:
            # убиваем, если таск выполняется дольше таймаута
            self.kill_after_timeout()
            # смотрим сколько сейчас активных процессов, пересоздаем, если меньше n_workers
            if len(active_children()) - 1 < self.n_workers:
                self.process_restart()
            # условие завершения мастер процесса: очередь закончилась для n_workers процессов
            # ИЛИ main послал сигнал в мастер процесс
            if self.signals_from_processes() or self.signal_from_main():
                # выключаем детей
                self.kill_all_children()
                return

    def make_worker(self) -> TaskProcessor:
        worker = TaskProcessor(
            self.t_queue,
            self.pid_task_start_time,
            self.q_get_timeout,
            self.q_timeouted)
        worker.daemon = True
        return worker

    def signals_from_processes(self) -> bool:
        queue_empty = len(self.q_timeouted)

        return queue_empty == self.n_workers

    def signal_from_main(self) -> bool:
        if self.main_conn.poll():
            # print("signal from main process!")
            self.main_conn.close()
            return True

    def kill_all_children(self):
        for worker in self.workers.values():
            worker.terminate()
            worker.join()

    def process_restart(self):
        new_workers_dict = {}
        for pid, worker in self.workers.items():
            if not worker.is_alive():
                # print("PID[{}] is not alive!".format(worker.pid))
                new_worker = self.make_worker()
                new_worker.start()
                # print("NEW WORKER CREATED WITH [{}]".format(new_worker.pid))

                new_workers_dict[new_worker.pid] = new_worker
            else:
                new_workers_dict[pid] = worker

        self.workers = new_workers_dict

    def kill_after_timeout(self):
        current_time = time.time()
        # из-за многопроцессорности ФРИЗИМ состояние дикта!
        pid_task_start_time_curr = copy.deepcopy(self.pid_task_start_time)
        # задержка для переходных процессов
        delay = 0.1
        for pid, task_start_time in pid_task_start_time_curr.items():
            if current_time - task_start_time - delay > self.timeout:
                # удаляем из словаря pid->task_start_time
                self.pid_task_start_time.pop(pid)
                # достаем из словаря воркеров, обновит словарь process_restart
                timeouted_worker = self.workers.get(pid)

                if timeouted_worker:
                    # убили процесс
                    # print("Killing {} worker".format(pid))
                    timeouted_worker.terminate()
                    # print("Killed {} worker".format(pid))
                    # чтобы не было зомби процесса
                    timeouted_worker.join()

# def targ_func(sleep_time, task_id):
#     print("TASK[{}] Started".format(task_id))
#     time.sleep(sleep_time)
#     print("TASK[{}] Ended".format(task_id))

# if __name__ == '__main__':
#     manager = Manager()
#     queue = manager.Queue()
#     main_conn, task_manager_conn = Pipe()
#
#     tasks = []
#     for i in range(10):
#         args = [1 + i, i]
#         task = Task(target_function=targ_func, args=args)
#         tasks.append(task)
#     tasks.append(Task(target_function=targ_func, args=[4,11]))
#
#     manager = TaskManager(queue, 2, task_manager_conn, timeout=5, q_get_timeout=10)
#     manager.start()
#
#     print("MANAGER started with [{}]".format(manager.pid))
#
#     for task in tasks:
#         queue.put(task)
#
#     time.sleep(50)
#
#     print("Killing manager!")
#     main_conn.send("terminate")
#     main_conn.close()
#     print("Manager died!")
#     manager.join()
