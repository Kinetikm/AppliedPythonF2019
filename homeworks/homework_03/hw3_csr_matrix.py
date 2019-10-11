import numpy as np
import copy


class CSRMatrix:

    def __init__(self, init_matrix_representation):
        self.IA = [0]
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.A = init_matrix_representation[2]
            self.JA = init_matrix_representation[1]
            self.num_col = max(init_matrix_representation[1]) + 1
            ia = init_matrix_representation[0]
            for i in self.A:
                if self.A[i] == 0:
                    del self.A[i]
                    del self.JA[i]
                    del ia[i]
            tmp = [0 for _ in range(max(ia)+1)]
            for i in ia:
                tmp[i] += 1
            sum_ = 0
            for j in range(len(tmp)):
                sum_ += tmp[j]
                self.IA.append(sum_)
        elif isinstance(init_matrix_representation, np.ndarray):
            self.A = list()
            self.JA = list()
            sum_ = 0
            for line in init_matrix_representation:
                for j in range(len(line)):
                    if line[j] != 0:
                        sum_ += 1
                        self.A.append(line[j])
                        self.JA.append(j)
                self.IA.append(sum_)
            self.num_col = len(init_matrix_representation[0])
        else:
            raise ValueError

    def get_idx(self, args):
        for idx in range(self.IA[args[0]], self.IA[args[0] + 1]):
            if self.JA[idx] == args[1]:
                return idx
        return None

    def __getitem__(self, args):
        r = self.get_idx(args)
        if r is not None:
            return self.A[r]
        return 0

    def __setitem__(self, args, item):
        if item != 0:
            for idx in range(self.IA[args[0]], self.IA[args[0] + 1]):
                if self.JA[idx] == args[1]:
                    self.A[idx] = item
                    return
                elif self.JA[idx] > args[1]:
                    self.JA.insert(idx, args[1])
                    self.A.insert(idx, item)
                    for i in range(args[0] + 1, len(self.IA)):
                        self.IA[i] += 1
                    return
            self.JA.insert(self.IA[args[0] + 1], args[1])
            self.A.insert(self.IA[args[0] + 1], item)
            for i in range(args[0] + 1, len(self.IA)):
                self.IA[i] += 1
        else:
            for idx in range(self.IA[args[0]], self.IA[args[0] + 1]):
                if self.JA[idx] == args[1]:
                    del self.JA[idx]
                    del self.A[idx]
                    for i in range(args[0] + 1, len(self.IA)):
                        self.IA[i] += -1
                    return

    def to_dense(self):
        out_list = list()
        for i in range(len(self.IA) - 1):
            line = list()
            for j in range(self.num_col):
                line.append(0)
            out_list.append(line)
        k = 0
        for i in range(1, len(self.IA)):
            for j in range(self.IA[i] - self.IA[i - 1]):
                out_list[i - 1][self.JA[k]] = self.A[k]
                k += 1
        return np.array(out_list)

    @property
    def nnz(self):
        return len(self.A)

    def __sub__(self, other):
        if self.num_col == other.num_col and len(self.IA) == len(other.IA):
            out = copy.deepcopy(other)
            out.A = other.A[::]
            out.IA = other.IA[::]
            out.JA = other.JA[::]
            for i in range(len(other.A)):
                out.A[i] *= -1
            k = 0
            for i in range(1, len(self.IA)):
                for j in range(self.IA[i] - self.IA[i - 1]):
                    idx = out.get_idx((i - 1, self.JA[k]))
                    if idx is not None:
                        if out.A[idx] + self.A[k] != 0:
                            out.A[idx] += self.A[k]
                        else:
                            out[(i - 1, self.JA[k])] = 0
                    else:
                        out[(i - 1, self.JA[k])] = self.A[k]
                    k += 1
            return out
        else:
            raise ValueError

    def __add__(self, other):
        if self.num_col == other.num_col and len(self.IA) == len(other.IA):
            out = copy.deepcopy(other)
            out.A = other.A[::]
            out.IA = other.IA[::]
            out.JA = other.JA[::]
            k = 0
            for i in range(1, len(self.IA)):
                for j in range(self.IA[i] - self.IA[i - 1]):
                    idx = out.get_idx((i - 1, self.JA[k]))
                    if idx is not None:
                        if out.A[idx] + self.A[k] != 0:
                            out.A[idx] += self.A[k]
                        else:
                            out[(i - 1, self.JA[k])] = 0
                    else:
                        out[(i - 1, self.JA[k])] = self.A[k]
                    k += 1
            return out
        else:
            raise ValueError

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            out = copy.deepcopy(self)
            out.A = self.A[::]
            out.IA = self.IA[::]
            out.JA = self.JA[::]
            for i in range(len(self.A)):
                out.A[i] *= other
        else:
            if self.num_col == other.num_col and len(self.IA) == len(other.IA):
                out = copy.deepcopy(self)
                out.A = self.A[::]
                out.IA = self.IA[::]
                out.JA = self.JA[::]
                k = 0
                for i in range(1, len(out.IA)):
                    for j in range(out.IA[i] - out.IA[i - 1]):
                        g_it = other[(i - 1, out.JA[k])]
                        if g_it != 0:
                            out.A[k] *= g_it
                        else:
                            out[(i - 1, out.JA[k])] = 0
                            k -= 1
                        k += 1
            else:
                raise ValueError
        return out

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            if other != 0:
                out = copy.deepcopy(self)
                out.A = self.A[::]
                out.IA = self.IA[::]
                out.JA = self.JA[::]
                for i in range(len(out.A)):
                    out.A[i] /= other
                return out
            else:
                raise ZeroDivisionError
        else:
            raise TypeError

    @staticmethod
    def transpose(other):
        real_vectors = [[] for _ in range(other.num_col)]
        int_vectors = [[] for _ in range(other.num_col)]
        new_A = list()
        new_IA = [0]
        new_JA = list()
        k = 0
        for i in range(1, len(other.IA)):
            for j in range(other.IA[i] - other.IA[i - 1]):
                int_vectors[other.JA[k]].append(i - 1)
                real_vectors[other.JA[k]].append(other.A[k])
                k += 1
        k = 0
        for i in range(len(real_vectors)):
            for j in range(len(real_vectors[i])):
                new_A.append(real_vectors[i][j])
                new_JA.append(int_vectors[i][j])
                k += 1
            new_IA.append(k)
        out = copy.deepcopy(other)
        out.A = new_A
        out.JA = new_JA
        out.IA = new_IA
        out.num_col = len(other.A)
        return out

    def __matmul__(self, other):
        if self.num_col == len(other.IA) - 1:
            new_A = list()
            new_IA = [0]
            new_JA = list()
            out = copy.deepcopy(self)
            out.num_col = other.num_col
            matr = self.transpose(other)
            matr_d = {}
            for i in range(len(matr.A)):
                k = 1
                while matr.IA[k] < i + 1:
                    k += 1
                matr_d[(k - 1, matr.JA[i])] = matr.A[i]
            ia = 0
            for i in range(0, len(self.IA) - 1):
                ja = 0
                for q in range(len(matr.IA) - 1):
                    sum_ = 0
                    for j in range(self.IA[i], self.IA[i + 1]):
                        if (q, self.JA[j]) in matr_d:
                            sum_ += self.A[j] * matr_d[(q, self.JA[j])]
                    if sum_ != 0:
                        new_A.append(sum_)
                        new_JA.append(ja)
                        ia += 1
                    ja += 1
                new_IA.append(ia)
            out.A = new_A
            out.JA = new_JA
            out.IA = new_IA
        else:
            raise ValueError
        return out
