#!/usr/bin/env python
# coding: utf-8


from multiprocessing import Pool
import os
import numpy as np
from scipy.sparse import csr_matrix
from pymorphy2 import MorphAnalyzer
import string


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
        raise NotImplementedError

    def idf(self, n, el):
        return np.log(n / el)

    def fit(self, folder, working_folder):
        '''
        Считаем idf, формируем словарь итп
        :param folder: string, путь до папки, в которой лежат текстовые файлы. (1 строка - один текст)
        Не ЗАБУДЬТЕ: убрать пунктуацию, привести слова к 1 регистру и форме
        FYI: pymorphy2, lower()
        :param working_folder: string, если у вас что-то не помешается в память (а оно не поместится =)), то дампим все
        в эту папку
        Работаем в числе потоков, равных n_jobs
        '''
        for key in list(words.keys()):
            if words[key] / N < self.min_df or words[key] / N > self.max_df:
                del words[key]
            else:
                words[key] = self.idf(N, words[key])
        words = np.array([(key, words[key]) for key in sorted(words)])
        with open(os.path.join(working_folder, "file"), 'wb') as f:
            pickle.dump(words, f)

    def transform(self, text):
        '''
        На входе текстовая строка, вам нужно вернуть её вектор (в спарс формате, чтобы в память поместился)
        :param text: string, строка, которую нужно закодировать
        !НЕ забудьте предобработать =)
        :return: sparse vector (используем scipy.csr_matrix)
        '''
        for punct in string.punctuation:
            text = text.replace(punct, ' ').lower()
        text = text.strip().split()
        text = [self.morph.parse(item)[0].normal_form for item in text]
        ngrams = zip(*[text[i:] for i in range(self.ngram_range[1])])
        text += [self.morph.parse("_".join(ngram))
                 [0].normal_form for ngram in ngrams]
        with open(os.path.join(self.working_folder, "file"), 'wb') as f:
            idfs = pickle.load(f)
        tf = Counter(text)
        res = np.array([0 if word not in tf else tf[word] * idf for word, idf in idfs])
        return csr_matrix(res)

    def idfs(self, output_file):
        '''
        Возвращаем все idfы у обученной модели, если она не обучена возвращаем пустой файл
        :param output_file: string, файл, в который нужно выгрузить idfы (слово \t idf)
        '''
        os.system(f"echo > {output_file}")
        with open(os.path.join(self.working_folder, "file"), 'rb') as f:
            words = pickle.load(f)
        with open(output_file, "w") as f:
            for word, idf in words:
                res = f"{word}\t{idf}\n"
                print(res)
                f.write(res)
