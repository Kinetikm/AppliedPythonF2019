#!/usr/bin/env python
# coding: utf-8


from multiprocessing import Pool
from functools import reduce
import os
from collections import Counter, defaultdict
from math import log
import pickle
import numpy as np
from scipy.sparse import csr_matrix
import string
from pymorphy2 import MorphAnalyzer


class TfIdfVectorizer:

    def __init__(self, min_df, max_df, ngram_range, n_jobs):
        '''
        Создаем экземлпяр класса с минимумом параметров
        :param min_df: float, минимальная доля документов, в которых должно втсретиться слово,
         чтобы мы начали его учитывать
        :param max_df: float, максимальная доля документов, в которых должно втсретиться слово,
         чтобы мы начали его учитывать
        :param ngram_range: tuple, берем пословные энграммы (от. до), Например: (1,1) значит берем только слова по 1
        :param n_jobs: число процессов (не потоков), с которыми должны выполнятсья дальнейшие преобразования.
        Если n_jobs = -1, то n_jobs = кол-во ядер
        '''
        self.min_df = min_df
        self.max_df = max_df
        self.ngram_range = ngram_range
        if n_jobs == -1:
            self.n_jobs = os.cpu_count()
        else:
            self.n_jobs = n_jobs
        self.working_folder = None
        self.morph = MorphAnalyzer()

    def fit(self, path_to_dir, working_folder):
        '''
        Считаем idf, формируем словарь итп
        :param folder: string, путь до папки, в которой лежат текстовые файлы. (1 строка - один текст)
        Не ЗАБУДЬТЕ: убрать пунктуацию, привести слова к 1 регистру и форме
        FYI: pymorphy2, lower()
        :param working_folder: string, если у вас что-то не помешается в память (а оно не поместится =)), то дампим все
        в эту папку
        Работаем в числе потоков, равных n_jobs
        '''
        working_file = f"{working_folder}/textfile_1"
        self.working_folder = working_folder
        os.system(f"echo > {working_file}")
        files = os.listdir(path_to_dir)
        pool = Pool(self.n_jobs)
        res = pool.map(self.read,
                       map(lambda file: os.path.join(path_to_dir, file),
                           files)
                       )
        words = reduce(lambda x, y: x + y[0], res, Counter())
        N = reduce(lambda x, y: x + y[1], res, 0)

        # print(words)
        for key in list(words.keys()):
            if words[key] / N < self.min_df or words[key] / N > self.max_df:
                del words[key]
            else:
                words[key] = np.log(N / words[key])
        # print(words)
        words = np.array([(key, words[key]) for key in sorted(words)])
        # print(words)
        # print(type(words))
        # raise AssertionError
        with open(os.path.join(working_folder, "file"), 'wb') as f:
            pickle.dump(words, f)

    def transform(self, text):
        '''
        На входе текстовая строка, вам нужно вернуть её вектор (в спарс формате, чтобы в память поместился)
        :param text: string, строка, которую нужно закодировать
        !НЕ забудьте предобработать =)
        :return: sparse vector (используем scipy.csr_matrix)
        '''
        text = self.preprocessing(text)
        with open(os.path.join(self.working_folder, "file"), 'wb') as f:
            idfs = pickle.load(f)
        tf = Counter(text)
        res = np.array([0 if word not in tf else tf[word] * idf for word, idf in idfs])
        return csr_matrix(res)

    def preprocessing(self, line):
        # line = self.morph.parse(line)[0].normal_form
        for punct in string.punctuation:
            line = line.replace(punct, ' ').lower()
        line = line.strip().split()
        line = [self.morph.parse(item)[0].normal_form for item in line]
        ngrams = zip(*[line[i:] for i in range(self.ngram_range[1])])
        line += [self.morph.parse("_".join(ngram))
                 [0].normal_form for ngram in ngrams]
        # print(line)
        return line

    def read(self, read_file):
        words = Counter()
        i = 0
        with open(read_file) as f:
            for line in f:
                line = self.preprocessing(line)
                words += Counter(set(line))
                i += 1
        return words, i

    def idfs(self, output_file):
        '''
        Возвращаем все idfы у обученной модели, если она не обучена возвращаем пустой файл
        :param output_file: string, файл, в который нужно выгрузить idfы (слово \t idf)
        '''
        if self.working_folder is None:
            return
        os.system(f"echo > {output_file}")
        with open(os.path.join(self.working_folder, "file"), 'rb') as f:
            words = pickle.load(f)
        with open(output_file, "w") as f:
            for word, idf in words:
                res = f"{word}\t{idf}\n"
                print(res)
                f.write(res)
