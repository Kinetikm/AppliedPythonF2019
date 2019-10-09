from os import listdir
from os.path import isfile, join
import multiprocessing
from multiprocessing import Pool, Manager, Queue


def count_words(queue, path):
    q = queue.get()
    name = path + '/' + q
    try:
        with open(name, 'r', encoding='utf8') as file:
            n_words = 0
            for line in file:
                words_list = line.split()
                n_words += len(words_list)
            queue.put((q, n_words))
    except (OSError, UnicodeDecodeError):
        queue.put((q, 0))


def word_count_inference(path_to_dir):
    dict_ = {'total': 0}
    process_count = 4
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(process_count)
    jobs = []
    len_ = 0
    for f in listdir(path_to_dir):
        if isfile(join(path_to_dir, f)):
            queue.put(f)
            len_ += 1
    for _ in range(len_):
        job = pool.apply_async(count_words, (queue, path_to_dir))
        jobs.append(job)
    for job in jobs:
        job.get()
    pool.close()
    pool.join()
    for _ in range(len_):
        q = queue.get()
        dict_[q[0]] = q[1]
        dict_['total'] += q[1]
    return dict_
