#!/usr/bin/env python
# coding: utf-8


import os
from multiprocessing import Manager, Process, Semaphore, cpu_count
import string
from pymorphy2 import MorphAnalyzer
from scipy.sparse import csr_matrix
import pickle
import numpy as np
import re


class TfIdfVectorizer:

    def __init__(self, min_df, max_df, ngram_range, n_jobs):
        self.min_df = min_df
        self.max_df = max_df
        self.ngram_range = ngram_range
        if n_jobs == -1:
            self.n_jobs = cpu_count()
        else:
            self.n_jobs = n_jobs
        self.d = None
        self.morph = MorphAnalyzer()

    def create_ngrams(self, line):
        for punct in string.punctuation:
            line = line.replace(punct, ' ').lower()
        splited_line = line.strip().split()
        ngrams = zip(*[splited_line[i:] for i in range(self.ngram_range[1])])
        splited_line += ["_".join(ngram) for ngram in ngrams]
        return splited_line

    def read_file(self, sem, path_to_dir, queue, word_list):
        with sem:
            filename = queue.get()
            counter = 0
            full_name = str(path_to_dir) + '/' + str(filename)
            with open(full_name) as f:
                for line in f:
                    counter += 1
                    splited_line = self.create_ngrams(line)
                    for i in range(len(splited_line)):
                        word = self.morph.parse(splited_line[i])[0].normal_form
                        splited_line[i] = word
                        if word not in word_list:
                            word_list[word] = 1
                        elif splited_line.count(word) == 1 or splited_line.index(word) == i:
                            word_list[word] += 1
            if "total_strings_number" in word_list:
                word_list["total_strings_number"] += counter
            else:
                word_list["total_strings_number"] = counter

    def word_count_inference(self, path_to_dir, dump_folder):
        manager = Manager()
        queue = manager.Queue()
        sem = Semaphore(self.n_jobs)

        tasks = []
        self.d = manager.dict()
        for filename in os.listdir(path_to_dir):
            queue.put(filename)
            proc = Process(target=self.read_file, args=(sem, path_to_dir, queue, self.d))
            tasks.append(proc)
            proc.start()
        for task in tasks:
            task.join()
        num_of_strings = self.d["total_strings_number"]
        keys = self.d.keys()
        for word in keys:
            self.d[word] /= num_of_strings
            if self.d[word] < self.min_df or self.d[word] > self.max_df:
                del self.d[word]
            else:
                self.d[word] = - np.log(self.d[word])
        return self.d

    def fit(self, folder, working_folder):
        self.word_count_inference(folder, working_folder)
        dump_path = working_folder + '/dict.pickle'
        with open(dump_path, 'wb') as f:
            pickle.dump(self.d, f)

    def transform(self, text):
        word_list = {}
        splited_line = self.create_ngrams(text)
        for i in range(len(splited_line)):
            word = self.morph.parse(splited_line[i])[0].normal_form
            splited_line[i] = word
            if word not in word_list:
                word_list[word] = 1
            else:
                word_list[word] += 1
        print(len(splited_line))
        data = np.zeros(len(splited_line))
        row_ind = np.zeros(len(splited_line))
        col_ind = np.zeros(len(splited_line))
        print(data, row_ind, col_ind)
        i = 0
        for word in word_list:
            word_list[word] /= len(splited_line)
            col = self.d.keys().index(word)
            col_ind[i] = col
            data[i] = word_list[word] * self.d[word]
            i += 1
        return csr_matrix((data, (row_ind, col_ind)), shape=(1, len(self.d)))

    def idfs(self, output_file):
        with open(output_file, 'w') as f:
            for word in self.d:
                    f.write(str(word) + "\t" + str(self.d[word]) + "\n")
