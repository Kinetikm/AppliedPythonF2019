#!/usr/bin/env python
# coding: utf-8

from homeworks.homework_04.hw4_wordcounter import word_count_inference
import math
import os
import time

import homeworks.homework_04.hw4_process_manager as pm
import multiprocessing


def test_output_dictionary():
    try:
        output = word_count_inference("./homeworks/homework_04/test_data")
    except NotImplementedError:
        return True
    answer = {'file_02': 0, 'file_06': 184, 'file_04': 209, 'file_03': 854, 'file_07': 607,
              'file_09': 4, 'file_01': 0, 'total': 2093, 'file_05': 235}
    for k, v in answer.items():
        assert k in output
        assert math.isclose(output[k], answer[k], rel_tol=0.05)


class SimpleTask(pm.Task):
    # qid = "spimple_task"

    def __init__(self, *args, **kwargs):
        # super().__init__(*args, qid=self.qid, **kwargs)
        super().__init__()

    def perform(self):
        print("worker pid:", os.getpid())
        time.sleep(1)
        print(f"worker {os.getpid()} done")


def test_task_processor():

    class TaskMock():
        def __init__(self, with_error=False):
            self.state = 'new'
            self.with_error = with_error

        def perform(self):
            assert self.state == 'locked', 'task is locked during performing'

            if self.with_error:
                raise Exception()

    class QMock():
        task = TaskMock()

        def get(self):
            return self.task

    qmock = QMock()
    tp = pm.TaskProcessor(qmock)
    tp.need_stop = 1

    time.sleep(0.01)
    assert tp.is_too_old(0), 'is too old'

    tp.run()
    assert qmock.task.state == 'done'

    qmock.task = TaskMock(with_error=True)
    tp.run()
    assert qmock.task.state == 'error'


def test_process_manager():

    with multiprocessing.Manager() as manager:
        queue = manager.Queue()
        tmanager = pm.TaskManager(queue, 2, 1.1, worker_graceful_shutdown_timeout=0.1, check_worker_alive_timeout=0.1)

        for i in range(4):
            task = SimpleTask()
            queue.put(task)

        run_start_time = time.time()
        tmanager.run(once=True)

        assert run_start_time - time.time() < 1.5
