def find_subarr(input_lst, num):
    if len(input_lst) == 0:
        return()
    cur_sum = 0
    sums = dict()
    # fill dict
    for i in range(len(input_lst)):
        cur_sum += input_lst[i]
        if cur_sum == num:
            return 0, i
        if cur_sum - num in sums:
            return sums[cur_sum - num] + 1, i
        else:
            sums[cur_sum] = i

    return()
