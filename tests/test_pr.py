#!/usr/bin/env python
# coding: utf-8

import unittest
import requests
import os
import re


class TestPrRules(unittest.TestCase):

    def check_pr_name(self):
        run_test = os.environ.get("TRAVIS_EVENT_TYPE", "not_travis")
        if run_test != "pull_request":
            return True
        pr_id = os.environ.get("TRAVIS_PULL_REQUEST", None)
        if not pr_id:
            return False
        pr_data = requests.get("https://api.github.com/repos/Kinetikm/AppliedPythonF2019/pulls/{}".format(pr_id))
        if pr_data.status_code != 200:
            raise Exception("Pull requests is not gotten. Ask your teacher to help")
        pr_data = pr_data.json()
        self.assertTrue(re.match("^hw(\d*)\s*(?:fixed|)\s*\w+\s*\w+$", pr_data['title'].lower()))
        self.assertEqual(pr_data['base']['ref'], pr_data['head']['ref'])
