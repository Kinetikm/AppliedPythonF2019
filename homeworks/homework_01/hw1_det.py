def calculate_determinant(list_of_lists):
    matrix = list_of_lists
    try:
        if type(matrix[0]) == list:
            for i in range(len(matrix)):
                if len(matrix) != len(matrix[i]):    # проверяем, является ли матрица квадратной
                    return None
        det = 0
        k = 1
        if len(matrix) > 2:
            for i in range(len(matrix)):
                minor = list()
                for j in range(len(matrix)-1):
                    minor.append(matrix[j+1][::])
                for j in range(len(matrix)-1):
                    del(minor[j][i])
                det = det + matrix[0][i]*k*calculate_determinant(minor)  # рекурсивно вычисляем определитель
                k = -k
            return det
        if len(matrix) == 2:
            det = matrix[0][0]*matrix[1][1] - matrix[1][0]*matrix[0][1]
            return det
        if len(matrix) == 1:
            if type(matrix[0]) == list:
                if len(matrix[0]) == 1:      # граничные условия для [[k]] и [k]
                    return matrix[0][0]
            if type(matrix[0]) == int:
                return matrix[0]
    except TypeError:
        return None

