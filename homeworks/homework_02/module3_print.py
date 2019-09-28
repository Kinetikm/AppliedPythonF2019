import ast


# функция для подсчета ширина для каждой колонки для json
def size_columns_json(data, titles):
    size_c = {}
    for i in range(len(data)):
        for j in titles:
            if j not in size_c:
                size_c[j] = len(str(data[i][j]))
            else:
                if len(str(data[i][j])) > size_c[j]:
                    size_c[j] = len(str(data[i][j]))
    for i in titles:
        if size_c[i] < len(i):
            size_c[i] = len(i)
    return size_c


# функция для подсчета ширина для каждой колонки для tsv
def size_columns_tsv(data, titles):
    count_c = len(titles)
    size_c = []
    for i in range(count_c):
        size_c.append(len(titles[i]))
    for i in range(count_c):
        for j in range(len(data)):
            if len(data[j][i]) > size_c[i]:
                size_c[i] = len(data[j][i])
    return size_c


def print_table(data, format_data):
    # если файл формата json
    if format_data == 'json':
        data = ast.literal_eval(data)
        titles = list(data[0].keys())
        size_c = size_columns_json(data=data, titles=titles)
        lines = sum(list(size_c.values()))  # подсчет кол-ва -
        count_c = len(list(size_c.values()))  # количество столбцов
        a = ['-'] * (lines + 4 * count_c + count_c + 1)  # вывод линии
        print(*a, sep='')
        print('|', end='', sep='')
        # вывод названий столбцов по центру
        for i in titles:
            print(i.center(2 + 2 + size_c[i]), end='|')
        print()
        # вывод данных
        for i in range(len(data)):
            print('|', end='')
            for j in titles:
                x = str(data[i][j])
                if j != titles[-1]:
                    print('  ', x.ljust(size_c[j] + 2), '|', end='', sep='')
                else:
                    print(x.rjust(2 + size_c[j], ' '), '  |', end='', sep='')
            print()
        print(*a, sep='')
    # если файл формата tsv
    elif format_data == 'tsv':
        data = data.split('\n')
        list_of_lists = []
        for i in data:
            x = i.split('\t')
            if x != ['']:
                list_of_lists.append(x)

        # вывод названия столбцов
        titles = list_of_lists[0]
        size_c = size_columns_tsv(data=list_of_lists[1::], titles=titles)
        count_c = len(titles)

        a = ['-'] * (sum(size_c) + count_c + 2 * count_c + 2 * count_c + 1)
        print(*a, sep='')
        print('|', end='')
        # вывод всех данных кроме последнего столбца
        for j in range(count_c - 1):
            x = str(list_of_lists[0][j])
            print(x.center(size_c[j] + 4), end='|', sep='')
        x = str(list_of_lists[0][count_c - 1])
        print(x.rjust(size_c[count_c - 1] + 2), '  ', end='|', sep='')
        print()
        # вывод последнего столбца
        for i in range(1, len(list_of_lists)):
            print('|', end='')
            for j in range(count_c - 1):
                x = str(list_of_lists[i][j])
                print('  ', x.ljust(size_c[j] + 2), end='|', sep='')
            x = str(list_of_lists[i][count_c - 1])
            print(x.rjust(size_c[count_c - 1] + 2), '  ', end='|', sep='')
            print()
        print(*a, sep='', end='')
