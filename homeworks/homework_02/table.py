#!/usr/bin/env python
# coding: utf-8


import sys
from builder import creator_of_tables

if __name__ == '__main__':
    filename = sys.argv[1]
    creator_of_tables(filename)
