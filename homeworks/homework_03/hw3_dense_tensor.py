from itertools import product


class Tensor:
    def __init__(self, matrix):
        self.matrix = matrix

    @classmethod
    def create_empty_tensor(cls, size):
        num_of_elements = 1
        for s in size:
            num_of_elements *= s
        empty_matrix = [0 for i in range(num_of_elements)]
        for i in range(1, len(size)):
            help_list = []
            for j in range(len(empty_matrix)):
                help_list.append(empty_matrix.pop(0))
                if (j + 1) % size[-i] == 0:
                    empty_matrix.append(help_list)
                    help_list = []
        return cls(empty_matrix)

    def size(self):
        size = [len(self.matrix)]
        element = self.matrix
        while isinstance(element[0], list):
            size.append(len(element[0]))
            element = element[0]
        return size

    def __setitem__(self, coordinates, item):
        if isinstance(coordinates, int):
            self.matrix[coordinates] = item
            return
        element = self.matrix
        for i in range(len(coordinates)-1):
            element = element[coordinates[i]]
        element[coordinates[-1]] = item

    def __getitem__(self, coordinates):
        if isinstance(coordinates, int):
            return self.matrix[coordinates]
        element = self.matrix
        for coor in coordinates:
            element = element[coor]
        return element

    def __calculator(self, value1, value2, oper):
        if oper == '+':
            return value1 + value2
        elif oper == '*':
            return value1 * value2
        else:
            return value1 ** value2

    def __calcul_result_of_oper(self, other, oper):
        size = self.size()
        coordinates = [range(max_idx) for max_idx in size]
        result = Tensor.create_empty_tensor(size)
        if isinstance(other, Tensor):
            if size != other.size():
                raise ValueError
            for coor in product(*coordinates):
                result[coor] = self.__calculator(self[coor], other[coor], oper)
        elif isinstance(other, int) or isinstance(other, float):
            for coor in product(*coordinates):
                result[coor] = self.__calculator(self[coor], other, oper)
        return result

    def __add__(self, other):
        return self.__calcul_result_of_oper(other, '+')

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self.__calcul_result_of_oper(other*(-1), '+')

    def __mul__(self, other):
        return self.__calcul_result_of_oper(other, '*')

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        return self.__calcul_result_of_oper(1/other, '*')

    def __pow__(self, other):
        return self.__calcul_result_of_oper(other, '^')

    def __consider_tensor(self, oper, axis=None):
        size = self.size()
        if axis is None:
            result = []
            coordinates = [range(max_idx) for max_idx in size]
            for coor in product(*coordinates):
                result.append(self[coor])
            if oper == 'sum':
                return sum(result)
            if oper == 'mean':
                return sum(result)/len(result)
            if oper == 'max':
                return max(result)
            if oper == 'min':
                return min(result)
            if oper == 'argmax':
                return result.index(max(result))
            if oper == 'argmin':
                return result.index(min(result))
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            result = Tensor.create_empty_tensor(size)
            for coor in product(*coordinates):
                lst = []
                coor = list(coor)
                for i in range(max_idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                if oper == 'sum':
                    result[coor] = sum(lst)
                elif oper == 'mean':
                    result[coor] = sum(lst)/len(lst)
                elif oper == 'max':
                    result[coor] = max(lst)
                elif oper == 'min':
                    result[coor] = min(lst)
                elif oper == 'argmax':
                    result[coor] = lst.index(max(lst))
                elif oper == 'argmin':
                    result[coor] = lst.index(min(lst))
            return result

    def sum(self, axis=None):
        return self.__consider_tensor('sum', axis)

    def mean(self, axis=None):
        return self.__consider_tensor('mean', axis)

    def max(self, axis=None):
        return self.__consider_tensor('max', axis)

    def min(self, axis=None):
        return self.__consider_tensor('min', axis)

    def argmax(self, axis=None):
        return self.__consider_tensor('argmax', axis)

    def argmin(self, axis=None):
        return self.__consider_tensor('argmin', axis)

    def transpose(self, *new_dimensions):
        size = self.size()
        new_size = [size[d] for d in new_dimensions]
        result = Tensor.create_empty_tensor(new_size)
        coordinates = [range(max_idx) for max_idx in size]
        for coor in product(*coordinates):
            new_coor = [coor[d] for d in new_dimensions]
            result[new_coor] = self[coor]
        return result

    def swapaxes(self, a1, a2):
        new_dim = list(range(len(self.size())))
        new_dim[a1], new_dim[a2] = new_dim[a2], new_dim[a1]
        return self.transpose(*new_dim)

    def __matmul__(self, other):
        l1, l2 = len(self.size()), len(other.size())
        if l1 > 2 or l2 > 2:
            raise ValueError
        tensor1 = Tensor([self.matrix]) if l1 == 1 else self
        tensor2 = Tensor([[el] for el in other.matrix]) if l2 == 1 else other
        num1_of_rows, num1_of_columns = tensor1.size()
        num2_of_rows, num2_of_columns = tensor2.size()
        if num1_of_columns != num2_of_rows:
            raise ValueError
        n = num1_of_columns
        tensor2 = tensor2.transpose(1, 0)
        result = Tensor.create_empty_tensor((num1_of_rows, num2_of_columns))
        for i, row1 in enumerate(tensor1.matrix):
            for j, row2 in enumerate(tensor2.matrix):
                result[i, j] = sum([row1[k]*row2[k] for k in range(n)])
        if l1 == 1:
            return Tensor(result.matrix[0])
        if l2 == 1:
            return Tensor([el[0] for el in result.matrix])
        return result
