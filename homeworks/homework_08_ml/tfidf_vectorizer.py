#!/usr/bin/env python
# coding: utf-8


import numpy
from scipy.sparse import csr_matrix


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
        self.ngram = ngram_range
        if n_jobs == -1:
            self.n_jobs = cpu_count()
        else:
            self.n_jobs = n_jobs

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
        pass

    def transform(self, text):
        '''
        На входе текстовая строка, вам нужно вернуть её вектор (в спарс формате, чтобы в память поместился)
        :param text: string, строка, которую нужно закодировать
        !НЕ забудьте предобработать =)
        :return: sparse vector (используем scipy.csr_matrix)
        '''
        pass

    def idfs(self, output_file):
        '''
        Возвращаем все idfы у обученной модели, если она не обучена возвращаем пустой файл
        :param output_file: string, файл, в который нужно выгрузить idfы (слово \t idf)
        '''
        pass
