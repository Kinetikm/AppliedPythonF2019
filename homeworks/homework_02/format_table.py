
def print_table(A):
    B = [""]*len(A[0])
    for line in A:
        for i in range(len(A[0])):
            if len(line[i]) > len(B[i]):
                B[i] = line[i]

    B = [len(i) for i in B]
    for i, w in enumerate(A[0]):
        A[0][i] = w.center(B[i])

    for line in A[1:]:
        for i, w in enumerate(line[:-1]):
            line[i] = w.ljust(B[i])
        line[-1] = line[-1].rjust(B[-1])

    s = '-'*(sum(B) + 5*len(A[1]) + 1)
    print(s)
    for line in A:
        ss = '|  ' + '  |  '.join(line) + '  |'
        print(ss)
    print(s)
