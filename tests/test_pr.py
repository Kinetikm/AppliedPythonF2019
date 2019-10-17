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
            return
        pr_data = pr_data.json()

        res = re.findall(r"^hw([1-9]+\d*)((?:\sweb|\sml|))(?:\sfixed|)\s[A-ZА-Я][a-zа-я]+\s[A-ZА-Я][a-zа-я]+$",
                         pr_data['title'])
        try:
            num_hw, track = res[0]
            num_hw = int(num_hw)
            if (track or num_hw > 4) and (not track or num_hw < 5):
                raise Exception()
        except Exception as e:
            raise Exception("Формат имени пулл-реквест не соответствует заданному")

        self.assertEqual(pr_data['base']['ref'], pr_data['head']['ref'],
                         msg="Какая-то хрень, почему не совпадают ветки пулл-реквеста?")
