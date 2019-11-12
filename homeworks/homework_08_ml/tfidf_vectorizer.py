#!/usr/bin/env python
# coding: utf-8
import math
import multiprocessing
import os
import numpy as np
import re
import scipy.sparse as sp
import pickle
from multiprocessing import Process, Queue
import pymorphy2


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

        self.tasks_queue = Queue()
        self.result_queue = Queue()
        self._min_df = min_df
        self._max_df = max_df
        self._ngram_range = ngram_range
        self.processes = []
        self._work_directory = None
        self._vocabulary = {}
        self._n_jobs = n_jobs if n_jobs != -1 else multiprocessing.cpu_count()

    def preprocess_reviews(self, line):
        return re.sub("[^а-яА-Яa-zA-Z]", ' ', line).lower()

    def remove_accented_chars(self, line):
        return re.sub(r'(ё|Ё)', 'е', line)

    def Morph(self, line):
        morph = pymorphy2.MorphAnalyzer()
        result = []
        line = self.remove_accented_chars(line)
        line = self.preprocess_reviews(line)
        for i in line.split():
            result.append(morph.parse(i)[0].normal_form)
        return result

    def preprocessing(self, folder):
        while not self.tasks_queue.empty():
            f_name = self.tasks_queue.get()
            keys = []
            ind = 0
            lines = 0
            with open(folder + "/" + f_name) as file_handler:
                for line in file_handler:

                    mod_line = self.Morph(line.strip())
                    lines += 1
                    for i in range(self._ngram_range[1] - self._ngram_range[0] + 1):
                        for j in range(0, len(mod_line) - i):
                            key = "_".join(mod_line[j:j + i + 1])
                            keys.append(key)
                        f = open(self._work_directory + '/' + f_name + str(ind) + '.pkl', 'wb')
                        pickle.dump(set(keys), f)
                        f.close()
                        keys.clear()
                        ind += 1
            self.result_queue.put(lines)
            lines = 0
            f = open(self._work_directory + '/' + f_name + str(ind) + '.pkl', 'wb')
            pickle.dump(keys, f)
            f.close()
            keys.clear()

    def fit(self, folder, working_folder):
        """
        Считаем idf, формируем словарь итп
        :param folder: string, путь до папки, в которой лежат текстовые файлы. (1 строка - один текст)
        Не ЗАБУДЬТЕ: убрать пунктуацию, привести слова к 1 регистру и форме
        FYI: pymorphy2, lower()
        :param working_folder: string, если у вас что-то не помешается в память (а оно не поместится =)), то дампим все
        в эту папку
        Работаем в числе потоков, равных n_jobs
        """
        res = 0
        self._work_directory = working_folder
        for i in os.listdir(folder):
            self.tasks_queue.put(i)

        for i in range(self._n_jobs):
            p = Process(target=self.preprocessing, args=(folder,))
            self.processes.append(p)
            p.start()

        for p in self.processes:
            p.join()

        for i in os.listdir(self._work_directory):
            with open(self._work_directory + '/' + i, "rb") as file_h:
                f = pickle.load(file_h)
                for line in f:
                    if line.strip() not in self._vocabulary:
                        self._vocabulary[line.strip()] = 0
                    self._vocabulary[line.strip()] += 1
                f.clear()

        while not self.result_queue.empty():
            res += self.result_queue.get()

        self._vocabulary = {k: (v, np.log((res / v))) for k, v in self._vocabulary.items()}
        return self

    def transform(self, text, normalize=True):
        '''
        На входе текстовая строка, вам нужно вернуть её вектор (в спарс формате, чтобы в память поместился)
        :param normalize:
        :param text: string, строка, которую нужно закодировать
        !НЕ забудьте предобработать =)
        :return: sparse vector (используем scipy.csr_matrix)
        '''
        j_indices = []
        indptr = [0]
        mod_line = self.Morph(text.strip())
        feature_counter = {}
        for i in range(self._ngram_range[1] - self._ngram_range[0] + 1):
            for j in range(0, len(mod_line) - i):
                key = "_".join(mod_line[j:j + i + 1])
                try:
                    feature_idx = self._vocabulary[key][0]
                    if feature_idx not in feature_counter:
                        feature_counter[feature_idx] = [0, self._vocabulary[key][1]]
                    feature_counter[feature_idx][0] += 1
                except KeyError:
                    continue
        j_indices.extend(feature_counter.keys())
        values = [i[0] * i[1] for i in feature_counter.values()]
        indptr.append(len(j_indices))

        j_indices = np.asarray(j_indices)
        indptr = np.asarray(indptr)
        values = np.asarray(values)

        X = sp.csr_matrix((values, j_indices, indptr),
                          shape=(len(indptr) - 1, len(self._vocabulary)))
        X.sort_indices()
        if normalize:
            self.normalize(X.data, X.shape, X.indptr)
        return X

    def idfs(self, output_file):
        '''
        Возвращаем все idfы у обученной модели, если она не обучена возвращаем пустой файл
        :param output_file: string, файл, в который нужно выгрузить idfы (слово \t idf)
        '''
        with open(output_file, "w") as f:
            for k, v in self._vocabulary.items():
                f.write(str(k) + '\t' + str(v[1]) + '\n')

    def normalize(self, X_data, shape, X_indptr):
        n_samples = shape[0]
        for i in range(n_samples):
            sum_ = 0.0
            for j in range(X_indptr[i], X_indptr[i + 1]):
                sum_ += (X_data[j] * X_data[j])

            if sum_ == 0.0:
                continue

            sum_ = math.sqrt(sum_)

            for j in range(X_indptr[i], X_indptr[i + 1]):
                X_data[j] /= sum_
