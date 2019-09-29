#!/usr/bin/env python
# coding: utf-8

import chardet


def encodingdetector(filename):
    with open(filename, 'rb') as f:
        encoding = chardet.detect(f.readline())['encoding']
        return encoding if encoding in ['utf-8', 'utf-16', 'windows-1251'] else None
