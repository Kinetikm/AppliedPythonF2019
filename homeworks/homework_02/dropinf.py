def out_table(data):
    '''Функция для вывода таблицы'''
    key = list(data.keys())
    length = 0
    mas_of_length = []
    val = list(data.values())
    error = 0
    # проверка на валидность данных
    if (len(key) == 0) or (len(val)) == 0:
        error = 1
    # количество столбцов должно совпадать
    for i in range(len(val) - 1):
        if len(val[i]) != len(val[i + 1]):
            error = 1
    if error == 1:
        print("Формат не валиден")
    else:
        # вычисление максимально возможной длины в каждом столбце
        mas_of_length = []
        for i in range(len(key)):
            max = len(key[i])
            for str in val[i]:
                if len(str) > max:
                    max = len(str)
            length += max
            mas_of_length.append(max)
        # вычисление ширины всей таблицы
        length += 5 * len(data) + 1
        # верхняя полоса
        line = ""
        for i in range(length):
            line += '-'
        print(line)
        # шапка
        body_line = "|"
        for i in range(len(key)):
            body_line += "  " + key[i].center(mas_of_length[i]) + "  |"
        print(body_line)
        # сама таблица
        body_line = "|"
        for i in range(len(val[0])):
            for j in range(len(key) - 1):
                body_line += "  " + val[j][i].ljust(mas_of_length[j]) + "  |"  # tut
            j = len(key) - 1
            body_line += "  " + val[j][i].rjust(mas_of_length[j]) + "  |"
            print(body_line)
            body_line = "|"
        # нижняя линия
        print(line)
