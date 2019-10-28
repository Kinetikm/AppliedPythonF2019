#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process
import time
import requests
import random
import string


class ProcessManager(Process):

    def __init__(self, tasks_queue, task_num, logger):
        super().__init__()
        self._task_queue = tasks_queue
        self._task_num = task_num
        self._tasks = []
        self._logger = logger

    def run(self):
        for i in range(self._task_num):
            job = ProcessProcessor(self._task_queue, self._logger, i)
            self._tasks.append(job)
            job.start()
        while True:
            time.sleep(5)
            tasks_tmp = []
            for i, job in enumerate(self._tasks):
                if not job.is_alive():
                    job = ProcessProcessor(self._task_queue, self._logger, i)
                    self._logger.info("Task restarted {}".format(i))
                    tasks_tmp.append(job)
                    job.start()
                else:
                    tasks_tmp.append(job)
            self._tasks = tasks_tmp


class ProcessProcessor(Process):

    def __init__(self, tasks_queue, logger, workerid):
        self.tasks_queue = tasks_queue
        self._workerid = workerid
        self._logger = logger
        self._users_ids = None
        self._actions = [1, 2, 3, 4, 5]
        super().__init__()

    def generate_users_ids(self, string_length):
        letters = string.ascii_lowercase + "0123456789"
        return ''.join(random.choice(letters) for i in range(string_length))

    def generate_user_ids(self):
        self._users_ids = set()
        for i in range(1000):
            self._users_ids.add(self.generate_users_ids(20))
        self._users_ids = list(self._users_ids)

    def run(self):
        while True:
            if self.tasks_queue.empty():
                time.sleep(2)
                continue
            try:
                query = self.tasks_queue.get(False)
            except queue.Empty:
                continue
            self._logger.info("Start processing for query {}".format(query))
            prev = None
            errors = False
            for c in range(10000):
                if prev and random.random() < 0.1:
                    res = requests.get("http://{}/stat")
                    if res.response_code != 200 or res.json().get('user') != prev['user'] or \
                            res.json().get('action') != prev['action'] or res.json().get('ts'):
                        self._logger.error("Bad result of get stat response for {}".format(query))
                        errors = True
                        break
                else:
                    action = random.choice(self._actions)
                    user = random.choice(self._users_ids)
                    res = requests.post("http://{}/stat", headers={"Content-Type": "application/json"},
                                        json={"user": user, "action": action})
                    if res.response_code != 200:
                        self._logger.error("Bad response for post stat {}".format(query))
                        errors = True
                        break
            if errors:
                self._logger.info("End processing for {} with errors".format(query))
            else:
                self._logger.info("Processing ended successfully {}".format(query))
