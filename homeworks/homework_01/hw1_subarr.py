def find_subarr(input_lst, num):
    i = 0
    j = 0
    z = 0
    for k in range(len(input_lst)):
        sum = 0
        for l in range(k, len(input_lst)):
            x = k
            sum += input_lst[l]
            if (sum == num):
                z = l
                return (x, z)
                break
    return()
