#!/usr/bin/env python
# coding: utf-8


from multiprocessing import Pool, Manager
import os


def cnt_file(queue, res_dict, cur_file, path_to_dir):
    with open(path_to_dir + '/' + cur_file, 'r') as file:
        val = 0
        for line in file:
            val += len(line.split())
        res_dict[cur_file] = val
        queue.put(val)


def cnt_all(queue, res_dict):
    tsum = 0
    while True:
        cur_sum = queue.get()
        if cur_sum == 'kill':
            break
        tsum += cur_sum
    res_dict['total'] = tsum
    return res_dict


def word_count_inference(path_to_dir):
    
    manager = Manager()
    res_dict = manager.dict()
    queue = manager.Queue()
   
    file_list = os.listdir(path=path_to_dir)
    pool = Pool(len(file_list) + 1)
    sum_of_all_proc = pool.apply_async(cnt_all, (queue, res_dict))

    proc_list = []
    for file in file_list:
        file_proc = pool.apply_async(cnt_file, (queue, res_dict, file, path_to_dir))
        proc_list.append(file_proc)
    for proc in proc_list:
        proc.get()

    queue.put('kill')

    res = dict(sum_of_all_proc.get())
    return res
