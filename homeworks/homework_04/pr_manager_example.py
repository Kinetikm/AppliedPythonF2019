from hw4_process_manager import Task, TaskManager
import multiprocessing
import time


def print_str(s):
    print(s)


def print_list(lst):
    for i in lst:
        print(i)


def produce_timeout(delay=5):
    time.sleep(delay)
    print("Opps! Process not terminated after timeout")


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    queue.put(Task(print_str, ('str 1',)))
    queue.put(Task(print_str, ('str 2',)))
    queue.put(Task(print_str, ('str 3',)))
    queue.put(Task(print_str, ('str 4',)))
    queue.put(Task(print_str, ('str 5',)))
    queue.put(Task(print_list, [1, 1, 1]))
    queue.put(Task(print_list, [2, 2, 2]))
    queue.put(Task(print_list, [3, 3, 3]))
    queue.put(Task(produce_timeout, **{'delay': 6}))
    queue.put(Task(produce_timeout, **{'delay': 3}))
    m = TaskManager(queue, n_workers=4, timeout=2)
    m.run()
