from multiprocessing import Process, Manager, Queue, Pool
import os


def worker(q, ret_d, path_to_dir):
    File = q.get()
    with open(path_to_dir + '/' + File, 'r', encoding='utf-8') as fin:
        count = 0
        for line in fin.readlines():
            count += len(line.split())
        ret_d[File] = count


def word_count_inference(path_to_dir):
    '''
    Метод, считающий количество слов в каждом файле из директории
    и суммарное количество слов.
    Слово - все, что угодно через пробел, пустая строка "" словом не считается,
    пробельный символ " " словом не считается. Все остальное считается.
    Решение должно быть многопроцессным. Общение через очереди.
    :param path_to_dir: путь до директории с файлами
    :return: словарь, где ключ - имя файла, значение - число слов +
        специальный ключ "total" для суммы слов во всех файлах
    '''
    files = os.listdir(path_to_dir)
    Process_num = 3
    manager = Manager()
    ret_d = manager.dict()
    q = manager.Queue()
    for File in files:
        q.put(File)
    pool = Pool(processes=Process_num)
    for _ in range(len(files)):
        pool.apply_async(worker, (q, ret_d, path_to_dir))
    pool.close()
    pool.join()
    ret_d["total"] = 0
    for v in ret_d.values():
        ret_d["total"] += v
    return ret_d
