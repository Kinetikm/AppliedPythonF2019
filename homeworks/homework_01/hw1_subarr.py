def find_subarr(input_lst, num):
    f = 0
    k = []
    for i in range(len(input_lst)):
        f += input_lst[i]
        k.insert(i, f)
        if k[0] == num:
            return(i, i)
    print(k)
    for j in range(len(k)):
        for l in range(j):
            if k[j] - k[l] == num:
                return(l+1, j)
