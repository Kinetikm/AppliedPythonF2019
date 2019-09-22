def find_subarr(input_lst, num):
    i = 0
    j = 0
    y = 0
    for i in range(len(input_lst)):
        sum = 0
        for j in range(i, len(input_lst)):
            x = i
            sum += input_lst[j]
            if (sum == num):
                y = j
                return (x, y)
                break
