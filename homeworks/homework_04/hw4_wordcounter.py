from multiprocessing import Manager, Queue
from multiprocessing import Pool
from os import listdir

PROCESSES_COUNT = 2


def func(x, path_to_dir="./homeworks/homework_04/test_data"):
    with open(path_to_dir + '/' + x, 'r', encoding='utf-8') as f:
        words = len(f.read().split())
    return words


def new_producer(path, queue):
    directory = path
    to_process_list = listdir(directory)
    for file in to_process_list:
        queue.put(file)
    queue.put('kill')


def new_consumer(results, queue: Queue):
    while True:
        file = queue.get()
        if file == 'kill':
            break
        num = func(file)
        results.put([num, file])


def returner(results):
    answer = {}
    total = 0
    while True:
        res = results.get()
        if res[0] == "kill":
            answer['total'] = total
            return answer
        answer[res[1]] = res[0]
        total += res[0]


def word_count_inference(path_to_dir="./test_data"):
    manager = Manager()
    queue = manager.Queue()
    results = manager.Queue()
    pool = Pool(PROCESSES_COUNT)

    pool.apply_async(new_consumer, (results, queue,))

    pool.apply_async(new_producer, (path_to_dir, queue)).get()

    pool.close()
    pool.join()
    results.put(["kill", "kill"])

    return returner(results)
