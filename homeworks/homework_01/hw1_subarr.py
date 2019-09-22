def find_subarr(input_lst, num):
    dict = {}
    sum = 0
    for i, var in enumerate(input_lst):
        sum += var
        if sum == num:
            return (0, i)
        elif sum - num in dict:
            return (dict[sum - num] + 1, i)
        dict[sum] = i
    return ()
