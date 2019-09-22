import copy


def delCol(matrix, i):  # Удалить i-ый столбец
    a = 0
    c = copy.deepcopy(matrix)
    while a < len(matrix):
        del c[a][i - 1]
        a += 1
    return c


def delRow(matrix, i):  # Удалить  i-ую строку
    a = 0
    c = copy.deepcopy(matrix)
    del c[i - 1]
    return c


def minor(matrix):  # Подсчет минора
    if len(matrix) == 2:
        result = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        print(result)
        return result
    else:
        return det(matrix)


def det(matrix):  # Определитель
    i = 1
    result = 0
    if len(matrix) == 2:
        return minor(matrix)
    while i <= len(matrix):
        result += (-1) ** (1 + i) * minor(delCol(delRow(matrix, 1), i)) * matrix[0][i - 1]
        i += 1
    return result


def calculate_determinant(list_of_lists):
    if len(list_of_lists) == 1 and type(list_of_lists[0]) is list and len(list_of_lists[0]) == 1 and type(
            list_of_lists[0][0]) is float:
        return list_of_lists[0][0]

    for i in list_of_lists:
        if type(i) is not list or len(i) != len(list_of_lists) or len(i) == 0:
            return "None"
        else:
            for j in i:
                if type(j) is not float:
                    return "None"

    else:
        n = len(list_of_lists)
        return det(list_of_lists)
