#!/usr/bin/env python
# coding: utf-8

import os
import tempfile
import subprocess

from utils.file_processors import PickleFileProcessor

from homeworks.homework_02.vkposter import VKPoster


def load_test_data(func_name):
    file_processor = PickleFileProcessor()
    test_filename = os.path.basename(__file__)
    test_filename = os.path.splitext(test_filename)[0]
    test_filename = os.path.join("tests/tests_data",
                                 test_filename + "_" + func_name + ".ini.pkl")
    output = file_processor.read_file(test_filename)
    return output


def test_vk_poster():
    data = load_test_data("vk_poster")
    try:
        vk_poster = VKPoster()
    except NotImplementedError:
        return True
    for test in data:
        vk_poster = VKPoster()
        for action, params, ans in zip(
                test['action'], test['params'], test['expected_ans']):
            if action == 'follow':
                assert ans == vk_poster.user_follow_for(*params)
            elif action == 'posted':
                assert ans == vk_poster.user_posted_post(*params)
            elif action == 'get_recent_posts':
                assert ans == vk_poster.get_recent_posts(*params)
            elif action == 'readed':
                assert ans == vk_poster.user_read_post(*params)
            elif action == 'get_most_popular_posts':
                assert ans == vk_poster.get_most_popular_posts(*params)
    return True


def test_table():
    data = load_test_data("table")

    for test_data, test_out in data:
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'wb') as tmp:
                tmp.write(test_data)

            out, err = subprocess.Popen(
                ['python', 'homeworks/homework_02/table.py', path],
                stdout=subprocess.PIPE,
            ).communicate()
            output = out.decode('utf8').strip()
            if output:
                assert test_out.strip() == output
            else:
                return True

        finally:
            os.remove(path)

    # Not Found
    out, err = subprocess.Popen(
        ['python', 'homeworks/homework_02/table.py', 'path'],
        stdout=subprocess.PIPE,
    ).communicate()
    assert 'Файл не валиден' == out.decode('utf8').strip()
    return True
