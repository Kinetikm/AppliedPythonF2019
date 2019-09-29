def print_table(title: tuple, rows: list):
    max_lst = list()
    for i in range(len(title)):
        max_lst.append(0)

    for row in rows:
        for i in range(len(row)):
            if len(row[i]) > max_lst[i]:
                max_lst[i] = len(row[i])

    for i in range(len(title)):
        if len(title[i]) > max_lst[i]:
            max_lst[i] = len(title[i])

    lenght = 0
    for x in max_lst:
        lenght += x

    lenght += (5 * (len(title) - 1)) + 6
    print('-' * lenght)

    #print(max_lst)
    #print(max_lst[3])
    for i, val in enumerate(title):
        if i != len(title):
            print(f'|  {val:^{max_lst[i]}}  ', end='')
        else:
            print(f'|  {val:^{max_lst[i]}}', end='')
    print('|')

    for row in rows:
        for i, val in enumerate(row):
            if i != len(row) - 1:
                print(f'|  {val:<{max_lst[i]}}  ', end='')
            else:
                print(f'|  {val:>{max_lst[i]}}', end='')
        print('  |')

    print('-' * lenght)
