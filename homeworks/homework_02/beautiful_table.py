from reading_file import csv_read, json_read


def cool_table(lst):
    '''
    Нашли длины столбцов, под которые нужно форматировать
    строки в столбцах
    '''
    pillarmen = [0 for i in range(len(lst[0]))]
    for i in range(len(lst[0])):
        pillarmen[i] = 0
        for j in range(len(lst)):
            if len(str(lst[j][i])) > pillarmen[i]:
                pillarmen[i] = len(lst[j][i])
    '''
    Переводим в строку, по пути добавляя знаки для красоты
    '''
    final_string = []
    string = ['' for i in range(len(lst))]
    for i in range(len(lst)):
        string[i] += '|  '
        for j in range(len(lst[i])):
            k = pillarmen[j]
            if i == 0:
                string[i] += '{:^{width}}'.format(str(lst[i][j]), width=k)
            elif j == (len(lst[i]) - 1):
                string[i] += '{:>{width}}'.format(str(lst[i][j]), width=k)
            else:
                string[i] += '{:{width}}'.format(str(lst[i][j]), width=k)
            if j != (len(lst[i]) - 1):
                string[i] += '  |  '
            else:
                string[i] += '  |'
    top = '-'*(len(string[0]))
    final_string.append(top)
    final_string += string
    final_string.append(top)
    return final_string
