from multiprocessing import Process, Queue
from time import sleep
from random import randint


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
        return self.func(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        super(TaskProcessor, self).__init__()
        self.tasks_q = tasks_queue
        self.timeout = timeout

    def run(self):
        """
        Старт работы воркера
        """
        while not self.tasks_q.empty():
            task = self.tasks_q.get()
            print(str(task), "start")
            process = Process(target=task.perform())
            process.start()
            process.join(timeout=self.timeout)
            process.terminate()
            print(str(task), "end")


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
        self.__queue = tasks_queue
        self.__n_workers = n_workers
        self.__timout = timeout
        self.__process = []

    def run(self):
        """
        Запускайте бычка! (с)
        """
        workers = [TaskProcessor(self.__queue, self.__timout) for _ in range(self.__n_workers)]
        for worker in workers:
            proc = Process(target=worker.run())
            self.__process.append(proc)
            proc.start()
        while not self.__queue.empty():
            self.__process[randint(0, len(self.__process) - 1)].terminate()
            for i, proc in enumerate(self.__process):
                if not proc.is_alive():
                    proc = Process(target=workers[i].run)
                    proc.start()
            sleep(5)


def cub(k):
    sleep(k)
    print(k ** 3)


q = Queue()
for i in range(7):
    q.put(Task(cub, i))
    print(f'put{i}')

tm = TaskManager(q, 7, 10)
proc = Process(target=tm.run, args=())
proc.start()

sleep(4)
for i in range(3, 8, 2):
    q.put(Task(cub, i))
    print(f'put{i}')

proc.join()
