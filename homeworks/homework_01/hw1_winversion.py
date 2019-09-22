def word_inversion(input_list):
    list = tuple(input_list)
    k = len(list)
    i = 0
    j = 0
    z = -1
    b = 0
    for i in range(k):
        z += 1
        if (list[i] == ' ' or i == (k - 1)):
            if (i == (k-1)):
                z += 1
            for j in range(z):
                if (i == (k-1)):
                    i += 1
                input_list[k - i + j] = list[b]
                b += 1
            if (i == k):
                i = i - 1
            if (list[i] == ' '):
                input_list[k - 1 - i] = list[b]
                b += 1
            z = -1
    return None
