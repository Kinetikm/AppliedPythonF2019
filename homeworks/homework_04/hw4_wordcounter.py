from multiprocessing import Process, Manager, Pool
import os


def words_in_file(path, filename, queue):
    sum = 0
    tmp = ()
    with open(path + "/" + filename, 'r') as file:
        sum = len(file.read().strip().split())
    tmp = (filename: sum)
    queue.put(tmp)
    return


def switch_queue(queue):
    total = 0
    main_dict = {}
    while True:
        res = queue.get()
        if res == 'end':
            break
        total += res[1]
        main_dict[res[0]] = res[1]
    main_dict['total'] = total
    return main_dict


def word_count_inference(path):
    count = os.cpu_count()
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(count)
    tasks = pool.apply_async(switch_queue, (queue, ))
    jobs = []
    for filename in os.listdir(path):
        if os.path.isfile(path + '/' + filename):
            job = pool.apply_async(words_in_file, (path, filename, queue))
            jobs.append(job)
    for job in jobs:
        job.get()
    queue.put('end')
    done_tasks = tasks.get()
    pool.close()
    pool.join()
    return done_tasks
