from multiprocessing import Queue
from hw4_process_manager import TaskManager, Task
import math
import time


def func_zero_arity():
    print("zero arity")


def func_one_arity(arg0):
    num = 1
    while True:
        time.sleep(0.3)
        print("{} one arity, period =  0.3 seconds, {} iteration".format(arg0, num))
        num += 1


def func_two_arity(arg0, arg1):
    num = 1
    while True:
        time.sleep(arg1)
        print(
            "{} two arity, period {} seconds, {} iteration".format(
                arg0, arg1, num))
        num += 1


def func_three_arity(arg0, arg1, arg2="default"):
    num = 1
    while True:
        time.sleep(arg1)
        print(
            "{} three arity, 3 parameter = {} period {} seconds, iteration {}".format(
                arg0,
                arg2,
                arg1,
                num))
        num += 1


if __name__ == "__main__":
    funcs = [
        Task(func_zero_arity),
        Task(func_one_arity, 1),
        Task(func_one_arity, 2),
        Task(func_two_arity, 3, 0.4),
        Task(func_one_arity, 4),
        Task(func_three_arity, 5, 0.4, "no default parameter"),
        Task(func_three_arity, 6, 0.3),
        Task(func_one_arity, 7),
        Task(func_two_arity, 8, 0.1),
        Task(func_one_arity, 9),
    ]

    q = Queue()
    for i in funcs:
        q.put(i)
    newTm = TaskManager(q, 5, 1)
    newTm.run()
    print("End TM run")
