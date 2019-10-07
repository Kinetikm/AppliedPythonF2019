import copy


class Tensor:
    def __init__(self, init_matrix_representation):
        self.matr = copy.deepcopy(init_matrix_representation)

    def __getitem__(self, index):
        if type(index) == tuple:
            return self.matr[index[0] - 1][index[1] - 1]  # c

    def __setitem__(self, key, value):
        self.matr[key[0]][key[1]] = value

    def __add__(self, other):
        if type(other) == float or type(other) == int:
            out = copy.deepcopy(self)
            for i in range(len(out.matr)):
                for j in range(len(out.matr[i])):
                    out[i, j] += other
            return out
        elif type(other) == Tensor:
            if (len(self.matr) == len(other.matr)) and (len(self.matr[0]) == len(other.matr[0])):
                out = copy.deepcopy(self)
                for i in range(len(out.matr)):
                    for j in range(len(out.matr[i])):
                        out[i, j] += other[i, j]
                return out
            else:
                raise ValueError
        raise ValueError

    def __sub__(self, other):
        if type(other) == float or type(other) == int:
            out = copy.deepcopy(self)
            for i in range(len(out.matr)):
                for j in range(len(out.matr[i])):
                    out[i, j] += other
            return out
        elif type(other) == Tensor:
            if (len(self.matr) == len(other.matr)) and (len(self.matr[0]) == len(other.matr[0])):
                out = copy.deepcopy(self)
                for i in range(len(out.matr)):
                    for j in range(len(out.matr[i])):
                        out[i, j] -= other[i, j]
                return out
            else:
                raise ValueError
        raise ValueError

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            out = copy.deepcopy(self)
            for i in range(len(out.matr)):
                for j in range(len(out.matr[i])):
                    out[i, j] += other
            return out
        elif type(other) == Tensor:
            if (len(self.matr) == len(other.matr)) and (len(self.matr[0]) == len(other.matr[0])):
                out = copy.deepcopy(self)
                for i in range(len(out.matr)):
                    for j in range(len(out.matr[i])):
                        out[i, j] = out[i, j] * other[i, j]
                return out
            else:
                raise ValueError
        raise ValueError

    def __truediv__(self, other):
        if other == 0:
            raise ValueError
        out = copy.deepcopy(self)
        for i in range(len(out.matr)):
            for j in range(len(out.matr[i])):
                out[i, j] = out[i, j]/other
        return out

    def __pow__(self, power, modulo=None):
        out = copy.deepcopy(self)
        for i in range(len(out.matr)):
            for j in range(len(out.matr[i])):
                if out[i, j] != 0:
                    out[i, j] = out[i, j]**power
        return out

    def sum(self, *axis):
        s = 0
        if len(axis) == 0:
            for i in range(len(self.matr)):
                for j in range(len(self.matr[i])):
                    s += self[i, j]
            return s
        else:
            for j in range(len(self.matr[axis[0]])):
                s += self[axis[0], j]
            return s

    def min(self, *axis):
        if len(axis) == 0:
            s = self[0, 0]
            for i in range(len(self.matr)):
                for j in range(len(self.matr[i])):
                    if self[i, j] < s:
                        s = self[i, j]
            return s
        else:
            s = self[axis[0], 0]
            for j in range(len(self.matr[axis[0]])):
                if self[axis[0], j] < s:
                    s = self[axis[0], j]
            return s

    def max(self, *axis):
        if len(axis) == 0:
            s = self.matr[0, 0]
            for i in range(len(self.matr)):
                for j in range(len(self.matr[i])):
                    if self[i, j] > s:
                        s = self[i, j]
            return s
        else:
            s = self[axis[0], 0]
            for j in range(len(self.matr[axis[0]])):
                if self[axis[0], j] > s:
                    s = self[axis[0], j]
            return s

    def argmin(self, *axis):
        if len(axis) == 0:
            s = self.matr[0, 0]
            p = 0
            for i in range(len(self.matr)):
                for j in range(len(self.matr[i])):
                    if self[i, j] < s:
                        s = self[i, j]
                        p = j
            return p

        m = self[axis[0], 0]
        m_i = 0
        for j in range(len(self.matr[axis[0]])):
            if self[axis[0], j] < m:
                m = self[axis[0], j]
                m_i = j
        return m_i

    def argmax(self, *axis):
        if len(axis) == 0:
            s = self.matr[0, 0]
            p = 0
            for i in range(len(self.matr)):
                for j in range(len(self.matr[i])):
                    if self[i, j] > s:
                        s = self[i, j]
                        p = j
            return p

        m = self[axis[0], 0]
        m_i = 0
        for j in range(len(self.matr[axis[0]])):
            if self[axis[0], j] > m:
                m = self[axis[0], j]
                m_i = j
        return m_i

    def mean(self, *axis):
        s = 0
        if len(axis) == 0:
            return self.sum()/(len(self.matr)*len(self.matr[0]))
        else:
            return self.sum(*axis)/(len(self.matr[0]))

    def transpose(self, *args):
        if (args is None) or ((args[0] == 1) and (args[1] == 0) == 0):
            new_m = []
            for i in range(len(self.matr[0])):
                new_m.append([0] * len(self.matr))
            for i in range(len(self.matr)):
                for j in range(len(self.matr[i])):
                    new_m[j][i] = self[i, j]
            self.matr = copy.deepcopy(new_m)

    def swapaxes(self, ax1, ax2):
        self.matr[ax1], self.matr[ax2] = self.matr[ax2], self.matr[ax1]

    def __matmul__(self, other):
        if (len(other.matr) == 1) and (len(other.matr[0]) == len(self.matr[0])):
            m = [[0] * len(self.matr)]
            for row in range(len(self.matr)):
                for i in range(len(self.matr[0])):
                    m[0][row] += self[row, i] * other[0, i]
            out = Tensor(m)
            return out

        if len(self.matr[0]) != len(other.matr):
            raise ValueError
        m = []
        for i in range(len(self.matr)):
            m.append([0] * len(other.matr[0]))
        out = Tensor(m)

        for row in range(len(self.matr)):
            for col in range(len(other.matr[0])):
                for i in range(len(self.matr[0])):
                    out[row, col] += self[row, i] * other[i, col]
        return out

    def get(self):
        return self.matr
