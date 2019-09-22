def find_subarr(input_lst, num):
    sols_dict = dict()
    sum1 = sum(input_lst)
    s = 0
    if num == sum1:
        return (0, len(input_lst) - 1)
    pred = 0
    for i, val in enumerate(input_lst):
        if val == num:
            return (i, i)
        if pred == num:
            return (0, i - 1)
        if sum1 - pred - val + num in sols_dict:
            return (sols_dict[sum1 - pred - val + num] + 1, i)
        else:
            s = sum1 - val - pred
            if s not in sols_dict:
                sols_dict[s] = i
            pred += val
    return()
