def find_subarr(input_lst, num):
    sums = 0
    sums_dict = dict()
    sums_dict[0] = -1
    for i in range(len(input_lst)):
        sums = sums + input_lst[i]
        if (sums - num) in sums_dict:
            p = (sums_dict[sums - num] + 1, i)
            return p
        else:
            sums_dict[sums] = i
    return ()
