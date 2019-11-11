#!/usr/bin/env python
# coding: utf-8


import os
from multiprocessing import Manager, Process, Semaphore, cpu_count
import string
from pymorphy2 import get_morph


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
        self.min_df = min_df
        self.max_df = max_df
        self.ngram_range = ngram_range
        if n_jobs == -1:
            self.n_jobs = cpu_count()
        else:
            self.n_jobs = n_jobs
        self.d = None


    def tfidf(self, ):
        pass
        # tf = n_word / n_all
        # idf = log(n_docs / docs_with_word)
        # tfidf = tf * idf

    def read_file(self, sem, path_to_dir, queue, d):
        with sem:
            filename = queue.get()
            word_list = {}
            counter = 0
            full_name = str(path_to_dir) + '/' + str(filename)
            morph = get_morph('dicts/ru')
            with open(full_name) as f:
                for line in f:
                    for punct in string.punctuation:
                        line = lower(line.replace(punct, ''))
                    splited_line = line.split()
                    for word in splited_line:
                        # counter += 1
                        word = morph(word)
                    for word in splited_line:
                        if word not in word_list:
                            word_list[word] = [splited_line.count(word) / len(splited_line), 1]
                            
            # словарь {слово : tf}
            for word in word_list:
                if count != 0:
                    word_list[word] /= count
            # словарь {filename : {слово : tf}}
            d[filename] = word_list

    def word_count_inference(self, path_to_dir, dump_folder):
        manager = Manager()
        queue = manager.Queue()
        sem = Semaphore(self.n_jobs)

        tasks = []
        self.d = manager.dict()
        for filename in os.listdir(path_to_dir):
            queue.put(filename)
            # sem.acquire()
            proc = Process(target=read_file, args=(sem, path_to_dir, queue, d))
            tasks.append(proc)
            proc.start()
        for task in tasks:
            task.join()
            # sem.release()
        return d

    def count_idf(self, word):
        return np.log(len(self.d.keys) / sum([1 for text in self.d if i word in text]))

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
        try:
            self.word_count_inference(folder, working_folder)
        except MemoryError:
            with open(working_folder  + "/dump.txt", 'w') as f:
                f.write(self.d)
                return
        for text in self.d:
            for word in text:
                text[word] *= self.count_idf(word)


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
