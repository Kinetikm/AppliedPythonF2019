def calculate_determinant(list_of_lists):
    matrix = list_of_lists
    det = 0
    k = 1
    try:
        if len(matrix) > 2:
            for i in range(len(matrix)):
                minor = list()
                for j in range(len(matrix) - 1):
                    minor.append(matrix[j + 1][::])
                for j in range(len(matrix) - 1):
                    del(minor[j][i])
                det = det + matrix[0][i] * k * calculate_determinant(minor)
                k = -k
            return det
        if len(matrix) == 2:
            det = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
            return det
        if len(matrix) == 1:
            return matrix[1]
    except KeyError:
        return None


'''
a = [[1, 2, 3], [4, 5, 6], [7, 35, 9]]
print(calculate_determinant(a))
'''
