def find_subarr(input_lst, num):
    dict = {}
    summ = 0
    for i in range(len(input_lst)):
        summ += input_lst[i]
        if (summ - num) in dict:
            return (dict[summ - num] + 1, i)
        if summ == num:
            return (0, i)
        dict[summ] = i
    return ()
