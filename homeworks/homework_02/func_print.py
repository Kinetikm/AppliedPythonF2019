def print_inf(data):
    length = []
    i = len(data)
    indent = 3
    m = len(data[0])
    for j in range(l):
        s = 0
        for k in range(i):
            if s < len(data[k][j]):
                s = len(data[k][j])
        length.append(s + 2 * indent)
    s = sum(length) - (m - 1)
    print(s * '-')
    begin = ''
    for j in range(m):
        spaces = int((length[j] - len(data[0][j]) - 2) / 2)
        begin += '|' + spaces * ' ' + data[0][j] + spaces * ' '
    begin += '|'
    print(begin)
    spaces = 2
    for x in range(1, i):
        string = ''
        for j in range(m):
            last = length[j] - len(data[x][j]) - 2 * spaces
            if j != m - 1:
                string += '|' + spaces * ' ' + data[x][j] + last * ' '
            else:
                string += '|' + last * ' ' + data[x][j] + spaces * ' '
        string += '|'
        print(string)
    print(s * '-')
