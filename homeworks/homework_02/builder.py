class Table:
    def draw(self, data):
        # ищем длину всей таблицы
        table_len = 0
        max_len_in_col = []  # здесь будут лежать длины наибольших элементов для каждой колонки
        for i in range(len(data[0])):
            column_elements = [str(data[j][i]) for j in range(len(data))]  # список состоящий из элементов одной колонки
            max_len = len(max(column_elements, key=len))  # ищем максимальную длину в данной колонке
            table_len += max_len
            max_len_in_col.append(max_len)
        table_len += 4*len(data[0]) + len(data[0]) + 1

        print('-' * table_len)

        # рисуем первую строчку с заголовками столбцов
        for j in range(len(data[0])):
            specificator = '|{:^%d}' % (max_len_in_col[j] + 4)
            print(specificator.format(data[0][j]), end='')
        print('|')

        # рисуем основную часть таблицы
        for i in range(1, len(data)):
            if len(data[i]) != len(data[0]):
                print('Формат не валиден')
                return
            else:
                for j in range(len(data[0])-1):
                    specificator = '|  {:<%d}' % (max_len_in_col[j] + 2)
                    print(specificator.format(data[i][j]), end='')

                specificator = '|{:>%d}  |' % (max_len_in_col[-1] + 2)
                print(specificator.format(data[i][-1]))
        print('-' * table_len)
