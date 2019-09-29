def print_table(table):
    width = []
    for i in range(len(table)):
        width.append(max(map(len, [x[i] for x in table])))

    for i, object in enumerate(table[0]):
        table[0][i] = object.center(width[i])

    for line in table[1:]:
        for i, object in enumerate(line[:-1]):
            line[i] = object.ljust(width[i])
        line[-1] = line[-1].rjust(width[-1])
    print('-'*(sum(width) + 5*len(table[1]) + 1))

    for line in table:
        print('|  ' + '  |  '.join(line) + '  |')

    print('-'*(sum(width) + 5*len(table[1]) + 1))
