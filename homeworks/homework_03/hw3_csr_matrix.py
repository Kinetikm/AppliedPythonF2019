import numpy as np


class CSRMatrix:
    def __init__(self, init_matrix):
        if isinstance(init_matrix, tuple) and len(init_matrix) == 3:
            row_ind, col_ind, data = init_matrix
            m, n = max(row_ind)+1, max(col_ind)+1
            num_of_elements = len(data)
            matrix = np.zeros((m, n))
            for i in range(num_of_elements):
                matrix[row_ind[i], col_ind[i]] = data[i]
            self.__init_from_np(matrix)
            self.__nnz = len(self.a)
        elif isinstance(init_matrix, np.ndarray):
            self.__init_from_np(init_matrix)
            self.n, self.m = init_matrix.shape
            self.__nnz = len(self.a)
        else:
            raise ValueError

    def __init_from_np(self, init_matrix):
        m, n = init_matrix.shape
        self.a = []
        self.ia = [0]
        self.ja = []
        for i in range(m):
            self.ia.append(self.ia[i])
            for j in range(n):
                if init_matrix[i][j]:
                    self.a.append(init_matrix[i][j])
                    self.ja.append(j)
                    self.ia[i+1] += 1

    @classmethod
    def create_empty_matrix(cls, num_of_rows):
        return cls(np.zeros((num_of_rows, 1)))

    @property
    def nnz(self):
        return self.__nnz

    def __check_coor(self, i, j):
        if not 0 <= i < len(self.ia)-1 or j < 0:
            raise ValueError

    def __getitem__(self, coor):
        i, j = coor
        self.__check_coor(i, j)
        for k in np.arange(self.ia[i], self.ia[i+1]):
            if self.ja[k] == j:
                return self.a[k]
        return 0

    def __setitem__(self, coor, value):
        i, j = coor
        self.__check_coor(i, j)
        element = self[coor]
        index = i + 1
        for k in np.arange(self.ia[i], self.ia[i+1]):
            if self.ja[k] == j:
                index = k
                break
        if value:
            if element:
                self.a[index] = value
            else:
                self.a.insert(self.ia[index], value)
                self.ja.insert(self.ia[index], j)
                for k in range(i+1, len(self.ia)):
                    self.ia[k] += 1
                self.__nnz += 1
        elif element:
            self.a.pop(index)
            self.ja.pop(index)
            for k in range(i+1, len(self.ia)):
                self.ia[k] -= 1
            self.__nnz -= 1

    def __sum(self, value1, value2):
        return value1 + value2

    def __dif(self, value1, value2):
        return value1 - value2

    def __calcul_add_or_sub(self, other, oper):
        num_of_rows = len(self.ia) - 1
        result = CSRMatrix.create_empty_matrix(num_of_rows)
        for i in range(1, len(self.ia)):
            for j in self.ja[self.ia[i-1]:self.ia[i]]:
                result[i-1, j] = self[i-1, j]
        for i in range(1, len(other.ia)):
            for j in other.ja[other.ia[i-1]:other.ia[i]]:
                result[i-1, j] = oper(result[i-1, j], other[i-1, j])
        return result

    def __add__(self, other):
        return self.__calcul_add_or_sub(other, self.__sum)

    def __sub__(self, other):
        return self.__calcul_add_or_sub(other, self.__dif)

    def __mul__(self, other):
        num_of_rows = len(self.ia) - 1
        result = CSRMatrix.create_empty_matrix(num_of_rows)
        if isinstance(other, CSRMatrix):
            for i in range(1, len(self.ia)):
                for j in self.ja[self.ia[i-1]:self.ia[i]]:
                    result[i-1, j] = self[i-1, j] * other[i-1, j]
        else:
            for i in range(1, len(self.ia)):
                for j in self.ja[self.ia[i-1]:self.ia[i]]:
                    result[i-1, j] = self[i-1, j] * other
        return result

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        return self * (1/other)

    def __matmul__(self, other):
        if self.m != other.n:
            raise ValueError
        result = CSRMatrix.create_empty_matrix(self.n)
        for i in range(self.n):
            for j in range(other.m):
                element = 0
                for k in range(self.ia[i], self.ia[i+1]):
                    element += self[i, self.ja[k]] * other[self.ja[k], j]
                result[i, j] = element
        return result

    def to_dense(self):
        m, n = len(self.ia)-1, max(self.ja)+1
        result = np.zeros((m, n))
        for i in range(m):
            for j in range(self.ia[i], self.ia[i+1]):
                result[i][self.ja[j]] = self.a[j]
        return result
