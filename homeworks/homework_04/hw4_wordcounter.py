from multiprocessing import Manager, Pool
import os


def word_count(filepath, queue):
    with open(filepath, 'r') as f:
        queue.put({filepath.split('/')[-1]: len(f.read().strip().split())})


def result_func(queue):
    res_dict = {}
    total = 0
    while True:
        result = queue.get()
        if result == "The end":
            break
        total += list(result.values())[0]
        res_dict.update(result)
    res_dict["total"] = total
    return res_dict


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

    NUMBER_OF_PROCESSES = 8
    manager = Manager()
    queue = manager.Queue()
    files = [os.path.join(path_to_dir, i) for i in os.listdir(path_to_dir)]
    pool = Pool(NUMBER_OF_PROCESSES)
    cons = pool.apply_async(result_func, (queue,))
    tot = [pool.apply_async(word_count, (filepath, queue)) for filepath in files]
    for elem in tot:
        elem.get()
    queue.put("The end")
    return cons.get()

