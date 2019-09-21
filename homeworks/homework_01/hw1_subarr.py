def find_subarr(input_lst, num):
    cur_sum = 0
    sums = dict()
    # fill set
    for i in range(len(input_lst)):
        cur_sum += input_lst[i]
        if cur_sum == num:
            return 0, i
        sums[cur_sum] = i

    for key in sums:
        if key - num in sums:
            return sums[key - num] + 1, sums[key]
    return()
