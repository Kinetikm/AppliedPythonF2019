#!/usr/bin/env python
# coding: utf-8

import unittest
import requests
import os
import re


class TestPrRules(unittest.TestCase):

    def test_pr_name(self):
        run_test = os.environ.get("TRAVIS_EVENT_TYPE", "not_travis")
        if run_test != "pull_request":
            return True
        pr_id = os.environ.get("TRAVIS_PULL_REQUEST", None)
        if not pr_id:
            return False
        pr_data = requests.get("https://api.github.com/repos/Kinetikm/AppliedPythonF2019/pulls/{}".format(pr_id))
        if pr_data.status_code != 200:
            raise Exception("Что-то сломалось, напиши преподу")
        pr_data = pr_data.json()
        self.assertTrue(re.match("^hw([1-9]+\d*)(?:\sfixed|)\s[A-ZА-Я][a-zа-я]+\s[A-ZА-Я][a-zа-я]+$", pr_data['title']),
                        msg="Формат имени пулл-реквест не соответствует заданному")
        self.assertEqual(pr_data['base']['ref'], pr_data['head']['ref'],
                         msg="Какая-то хрень, почему не совпадают ветки пулл-реквеста?")
