from itertools import product


class Tensor:

    def __init__(self, init_matrix_representation):
        self.vector = init_matrix_representation
        self.tensor_sizes = self.get_tensor_sizes(self.vector)
        self.vector = self.matrix_to_list(self.vector)

    def matrix_to_list(self, matrix):
        list_ = list()
        for idx in product(*[range(i) for i in self.get_tensor_sizes(matrix)]):
            if isinstance(idx, int):
                list_.append(matrix[idx])
            else:
                tmp = matrix
                for j in idx:
                    tmp = tmp[j]
                list_.append(tmp)
        return list_

    @staticmethod
    def list_to_matrix(list_, tensor_sizes):
        if len(tensor_sizes) == 1:
            return list_
        tmp = list_[::]
        matrix = list()
        for j in tensor_sizes[:0:-1]:
            matrix = list()
            for i in range(0, len(tmp), j):
                matrix.append([tmp[k] for k in range(i, i+j)])
            tmp = matrix[::]
        return matrix

    @staticmethod
    def get_list_idx(args, tensor_sizes):
        if isinstance(args, int):
            return args
        idx = 0
        k = 1
        try:
            for i in range(len(args)):
                idx += (args[-i - 1]) * k
                k = k * tensor_sizes[-i - 1]
        except IndexError:
            pass
        return idx

    def __getitem__(self, args):
        return self.vector[self.get_list_idx(args, self.tensor_sizes)]

    def __setitem__(self, args, item):
        self.vector[self.get_list_idx(args, self.tensor_sizes)] = item

    def __sub__(self, other):
        out_list = list()
        if isinstance(other, int) or isinstance(other, float):
            for i in range(len(self.vector)):
                out_list.append(self.vector[i] - other)
            return Tensor(self.list_to_matrix(out_list, self.tensor_sizes))
        else:
            other.vector = self.matrix_to_list(other.vector)
            try:
                for i in range(len(self.vector)):
                    out_list.append(self.vector[i] - other.vector[i])
            except IndexError:
                raise ValueError
        return Tensor(self.list_to_matrix(out_list, self.tensor_sizes))

    def __add__(self, other):
        out_list = list()
        if isinstance(other, int) or isinstance(other, float):
            for i in range(len(self.vector)):
                out_list.append(self.vector[i] + other)
            return Tensor(self.list_to_matrix(out_list, self.tensor_sizes))
        else:
            other.vector = self.matrix_to_list(other.vector)
            try:
                for i in range(len(self.vector)):
                    out_list.append(self.vector[i] + other.vector[i])
            except IndexError:
                raise ValueError
        return Tensor(self.list_to_matrix(out_list, self.tensor_sizes))

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        out_list = list()
        if isinstance(other, int) or isinstance(other, float):
            for i in range(len(self.vector)):
                out_list.append(self.vector[i] * other)
            return Tensor(self.list_to_matrix(out_list, self.tensor_sizes))

        other.vector = self.matrix_to_list(other.vector)
        try:
            for i in range(len(self.vector)):
                out_list.append(self.vector[i] * other.vector[i])
        except IndexError:
            raise ValueError
        return Tensor(self.list_to_matrix(out_list, self.tensor_sizes))

    def __pow__(self, other):
        out_list = list()
        for i in range(len(self.vector)):
            out_list.append(self.vector[i] ** other)
        return Tensor(self.list_to_matrix(out_list, self.tensor_sizes))

    def __truediv__(self, other):
        out_list = list()
        for i in range(len(self.vector)):
            out_list.append(self.vector[i] / other)
        return Tensor(self.list_to_matrix(out_list, self.tensor_sizes))

    @staticmethod
    def get_tensor_sizes(vector):
        sizes = list()
        try:
            tmp = vector[0]
        except (TypeError, IndexError):
            sizes.append(0)
            return sizes
        sizes.append(len(vector))
        if len(vector) != 0:
            try:
                while True:
                    sizes.append(len(tmp))
                    tmp = tmp[0]
            except (TypeError, IndexError):
                pass
            return sizes

    def sum(self, axis=None):
        if axis is None:
            return sum(self.vector)
        else:
            size = self.tensor_sizes[::]
            idx = size.pop(axis)
            k = 1
            for i in size:
                k *= i
            out_list = [0 for _ in range(k)]
            coordinates = [range(idx) for idx in size]
            for indx in product(*coordinates):
                lst = []
                coor = list(indx)
                for i in range(idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                out_list[self.get_list_idx(indx, size)] = sum(lst)
        return Tensor(self.list_to_matrix(out_list, size))

    def mean(self, axis=None):
        if axis is None:
            return sum(self.vector)/len(self.vector)
        else:
            size = self.tensor_sizes[::]
            idx = size.pop(axis)
            k = 1
            for i in size:
                k *= i
            out_list = [0 for _ in range(k)]
            coordinates = [range(idx) for idx in size]
            for indx in product(*coordinates):
                lst = []
                coor = list(indx)
                for i in range(idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                out_list[self.get_list_idx(indx, size)] = sum(lst)/len(lst)
        return Tensor(self.list_to_matrix(out_list, size))

    def max(self, axis=None):
        if axis is None:
            return max(self.vector)
        else:
            size = self.tensor_sizes[::]
            idx = size.pop(axis)
            k = 1
            for i in size:
                k *= i
            out_list = [0 for _ in range(k)]
            coordinates = [range(idx) for idx in size]
            for indx in product(*coordinates):
                lst = []
                coor = list(indx)
                for i in range(idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                out_list[self.get_list_idx(indx, size)] = max(lst)
        return Tensor(self.list_to_matrix(out_list, size))

    def min(self, axis=None):
        if axis is None:
            return min(self.vector)
        else:
            size = self.tensor_sizes[::]
            idx = size.pop(axis)
            k = 1
            for i in size:
                k *= i
            out_list = [0 for _ in range(k)]
            coordinates = [range(idx) for idx in size]
            for indx in product(*coordinates):
                lst = []
                coor = list(indx)
                for i in range(idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                out_list[self.get_list_idx(indx, size)] = min(lst)
        return Tensor(self.list_to_matrix(out_list, size))

    def argmax(self, axis=None):
        if axis is None:
            return self.vector.index(max(self.vector))
        else:
            size = self.tensor_sizes[::]
            idx = size.pop(axis)
            k = 1
            for i in size:
                k *= i
            out_list = [0 for _ in range(k)]
            coordinates = [range(idx) for idx in size]
            for indx in product(*coordinates):
                lst = []
                coor = list(indx)
                for i in range(idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                out_list[self.get_list_idx(indx, size)] = lst.index(max(lst))
        return Tensor(self.list_to_matrix(out_list, size))

    def argmin(self, axis=None):
        if axis is None:
            return self.vector.index(min(self.vector))
        else:
            size = self.tensor_sizes[::]
            idx = size.pop(axis)
            k = 1
            for i in size:
                k *= i
            out_list = [0 for _ in range(k)]
            coordinates = [range(idx) for idx in size]
            for indx in product(*coordinates):
                lst = []
                coor = list(indx)
                for i in range(idx):
                    coor.insert(axis, i)
                    lst.append(self[coor])
                    coor.pop(axis)
                out_list[self.get_list_idx(indx, size)] = lst.index(min(lst))
        return Tensor(self.list_to_matrix(out_list, size))

    def transpose(self, *new_coord):
        new_sizes = [self.tensor_sizes[d] for d in new_coord]
        k = 1
        for i in new_sizes:
            k *= i
        out_list = [0 for _ in range(k)]
        coord = [range(max_idx) for max_idx in self.tensor_sizes]
        for idx in product(*coord):
            new_ = [idx[j] for j in new_coord]
            out_list[self.get_list_idx(new_, new_sizes)] = self[idx]
        return Tensor(self.list_to_matrix(out_list, new_sizes))

    def swapaxes(self, i, j):
        axes = [k for k in range(len(self.tensor_sizes))]
        axes[i], axes[j] = axes[j], axes[i]
        return self.transpose(*axes)

    def __matmul__(self, other):
        if len(self.tensor_sizes) == 1:
            num_str1 = 1
            num_col1 = self.tensor_sizes[0]
            if other.tensor_sizes[0] != self.tensor_sizes[0]:
                raise ValueError
        else:
            num_str1 = self.tensor_sizes[0]
            num_col1 = self.tensor_sizes[1]
            if other.tensor_sizes[0] != self.tensor_sizes[1]:
                raise ValueError
        oth_vect = Tensor(self.list_to_matrix(other.vector, other.tensor_sizes))
        if len(other.tensor_sizes) == 1:
            num_col2 = 1
            oth_vect = Tensor([[i] for i in oth_vect.vector])
        else:
            num_col2 = other.tensor_sizes[1]
        out_list = [0 for _ in range(num_str1 * num_col2)]
        for i in range(num_col2):
            for k in range(num_str1):
                s = 0
                for j in range(num_col1):
                    try:
                        s += oth_vect[j, i] * self[k, j]
                    except IndexError:
                        break
                new_ = (k, i)
                out_list[self.get_list_idx(new_, [num_str1, num_col2])] = s
        if num_col2 == 1 or num_str1 == 1:
            return Tensor(out_list)
        return Tensor(self.list_to_matrix(out_list, [num_str1, num_col2]))
