#!/usr/bin/env python
# coding: utf-8

from abc import ABC, abstractmethod

import gzip
import pickle


class FileProcessor(ABC):

    @abstractmethod
    def read_file(self, filename):
        pass

    @abstractmethod
    def write_file(self, filename, data):
        pass


class TarFileProcessor(FileProcessor):

    def read_file(self, filename):
        with gzip.open(filename, 'rb') as f:
            file_content = f.read()
        return file_content.decode("utf-8").split("\n")

    def write_file(self, filename, data):
        with gzip.open(filename, 'wb') as f:
            f.write(data.encode("utf-8"))


class PickleFileProcessor(FileProcessor):

    def read_file(self, filename):
        with open(filename, "rb") as f:
            file_content = pickle.load(f)
        return file_content

    def write_file(self, filename, data):
        with open(filename, "wb") as f:
            pickle.dump(data, f, protocol=pickle.DEFAULT_PROTOCOL)
