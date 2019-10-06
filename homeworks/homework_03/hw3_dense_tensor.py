from itertools import product


class Tensor:
    """
    Your realisation of numpy tensor.

    Must be implemented:
    1. Getting and setting element by indexes of row and col.
    a[i, j] = v -- set value in i-th row and j-th column to value.
    b = a[i, j] -- get value from i-th row and j-th column.
    2. Pointwise operations.
    c = a + b -- sum of two Tensors of the same shape or sum with scalar.
    c = a - b -- difference --//--.
    c = a * b -- product --//--.
    c = a / alpha -- divide Tensor a by nonzero scalar alpha.
    c = a ** b -- raises each element of a to the power b.
    3. Sum, mean, max, min, argmax, argmin by axis.
    if axis is None then operation over all elements.
    4. Transpose by given axes (by default reverse dimensions).
    5. Swap two axes.
    6. Matrix multiplication for tensors with dimension <= 2.
    """
    def __init__(self, matrix):
        """
        :param init_matrix_representation: list of lists
        """
        self.matrix = matrix
        self.sizes = []
        self.dim = self.def_dim(matrix)

    def def_dim(self, matrix, dim=0):
        if isinstance(matrix, list):
            if not matrix:
                return dim
            dim += 1
            self.sizes.append(len(matrix))
            dim = self.def_dim(matrix[0], dim)
            return dim
        else:
            # нужно ли возвращать None, если dim == 0?
            return dim

    def size(self):
        size = [len(self.matrix)]
        element = self.matrix
        while isinstance(element[0], list):
            size.append(len(element[0]))
            element = element[0]
        return size

    def __getitem__(self, coordinates):
        if isinstance(coordinates, int):
            return self.matrix[coordinates]
        element = self.matrix
        for coor in coordinates:
            element = element[coor]
        return element

    def __setitem__(self, coordinates, item):
        if isinstance(coordinates, int):
            self.matrix[coordinates] = item
            return
        element = self.matrix
        for i in range(len(coordinates)-1):
            element = element[coordinates[i]]
        element[coordinates[-1]] = item

    def __add__(self, other):
        size = self.size()
        coordinates = [range(max_idx) for max_idx in size]
        result = Tensor.create(size)
        if isinstance(other, Tensor):
            if size != other.size():
                raise ValueError
            for coor in product(*coordinates):
                result[coor] = self[coor] + other[coor]
        elif isinstance(other, int) or isinstance(other, float):
            for coor in product(*coordinates):
                result[coor] = self[coor] + other
        return result

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        size = self.size()
        coordinates = [range(max_idx) for max_idx in size]
        result = Tensor.create(size)
        if isinstance(other, Tensor):
            if size != other.size():
                raise ValueError
            for coor in product(*coordinates):
                result[coor] = self[coor] - other[coor]
        elif isinstance(other, int) or isinstance(other, float):
            for coor in product(*coordinates):
                result[coor] = self[coor] - other
        return result

    def __mul__(self, other):
        size = self.size()
        coordinates = [range(max_idx) for max_idx in size]
        result = Tensor.create(size)
        if isinstance(other, Tensor):
            if size != other.size():
                raise ValueError
            for coor in product(*coordinates):
                result[coor] = self[coor] * other[coor]
        elif isinstance(other, int) or isinstance(other, float):
            for coor in product(*coordinates):
                result[coor] = self[coor] * other
        return result

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        size = self.size()
        coordinates = [range(max_idx) for max_idx in size]
        result = Tensor.create(size)
        if isinstance(other, Tensor):
            if size != other.size():
                raise ValueError
            for coor in product(*coordinates):
                result[coor] = self[coor] / other[coor]
        elif isinstance(other, int) or isinstance(other, float):
            for coor in product(*coordinates):
                result[coor] = self[coor] / other
        return result

    def __pow__(self, other):
        size = self.size()
        coordinates = [range(max_idx) for max_idx in size]
        result = Tensor.create(size)
        if isinstance(other, Tensor):
            if size != other.size():
                raise ValueError
            for coor in product(*coordinates):
                result[coor] = self[coor] ** other[coor]
        elif isinstance(other, int) or isinstance(other, float):
            for coor in product(*coordinates):
                result[coor] = self[coor] ** other
        return result

    def sum(self, axis=None):
        size = self.size()
        if axis is None:
            result = []
            coordinates = [range(max_idx) for max_idx in size]
            for coor in product(*coordinates):
                result.append(self[coor])
            max_el, min_el = max(result), min(result)
            return sum(result)
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            result = Tensor.create(size)
            for coor in product(*coordinates):
                lst = []
                coor = list(coor)
                for i in range(max_idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                result[coor] = sum(lst)
            return result

    def mean(self, axis=None):
        size = self.size()
        if axis is None:
            result = []
            coordinates = [range(max_idx) for max_idx in size]
            for coor in product(*coordinates):
                result.append(self[coor])
            max_el, min_el = max(result), min(result)
            return sum(result)/len(result)
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            result = Tensor.create(size)
            for coor in product(*coordinates):
                lst = []
                coor = list(coor)
                for i in range(max_idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                result[coor] = sum(lst)/len(lst)
            return result

    def max(self, axis=None):
        size = self.size()
        if axis is None:
            result = []
            coordinates = [range(max_idx) for max_idx in size]
            for coor in product(*coordinates):
                result.append(self[coor])
            max_el, min_el = max(result), min(result)
            return max_el
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            result = Tensor.create(size)
            for coor in product(*coordinates):
                lst = []
                coor = list(coor)
                for i in range(max_idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                result[coor] = max(lst)
            return result

    def min(self, axis=None):
        size = self.size()
        if axis is None:
            result = []
            coordinates = [range(max_idx) for max_idx in size]
            for coor in product(*coordinates):
                result.append(self[coor])
            max_el, min_el = max(result), min(result)
            return min_el
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            result = Tensor.create(size)
            for coor in product(*coordinates):
                lst = []
                coor = list(coor)
                for i in range(max_idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                result[coor] = min(lst)
            return result

    def argmax(self, axis=None):
        size = self.size()
        if axis is None:
            result = []
            coordinates = [range(max_idx) for max_idx in size]
            for coor in product(*coordinates):
                result.append(self[coor])
            max_el, min_el = max(result), min(result)
            return result.index(max_el)
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            result = Tensor.create(size)
            for coor in product(*coordinates):
                lst = []
                coor = list(coor)
                for i in range(max_idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                result[coor] = lst.index(max(lst))
            return result

    def argmin(self, axis=None):
        size = self.size()
        if axis is None:
            result = []
            coordinates = [range(max_idx) for max_idx in size]
            for coor in product(*coordinates):
                result.append(self[coor])
            max_el, min_el = max(result), min(result)
            return result.index(min_el)
        else:
            max_idx = size.pop(axis)
            coordinates = [range(max_idx) for max_idx in size]
            result = Tensor.create(size)
            for coor in product(*coordinates):
                lst = []
                coor = list(coor)
                for i in range(max_idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                result[coor] = lst.index(min(lst))
            return result

    @classmethod
    def create(cls, size):
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

    def transpose(self, *new_dimensions):
        size = self.size()
        new_size = [size[d] for d in new_dimensions]
        result = Tensor.create(new_size)
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
        tensor1 = Tensor([self.matrix]) if l1 == 1 else self
        tensor2 = Tensor([[el] for el in other.matrix]) if l2 == 1 else other
        num1_of_rows, num1_of_columns = tensor1.size()
        num2_of_rows, num2_of_columns = tensor2.size()
        if num1_of_columns != num2_of_rows:
            raise ValueError
        n = num1_of_columns
        tensor2 = tensor2.transpose(1, 0)
        result = Tensor.create((num1_of_rows, num2_of_columns))
        for i, row1 in enumerate(tensor1.matrix):
            for j, row2 in enumerate(tensor2.matrix):
                result[i, j] = sum([row1[k]*row2[k] for k in range(n)])
        result = Tensor(result.matrix[0]) if l1 == 1 else result
        result = Tensor([el[0] for el in result.matrix]) if l2 == 1 else result
        return result
