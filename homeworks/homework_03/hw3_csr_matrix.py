import copy
import numpy as np


class CSRMatrix(object):
    def __init__(self, init_matrix_representation):

        # from dense
        if isinstance(init_matrix_representation, np.ndarray):
            self.items = []
            self.amounts = [0]
            self.col_indxs = []
            for i in range(len(init_matrix_representation)):
                # check iterators
                self.amounts.append(self.amounts[-1])  # copy prev item
                for j in range(len(init_matrix_representation[0])):
                    if init_matrix_representation[i][j] != 0:
                        self.amounts[-1] += 1
                        self.items.append(init_matrix_representation[i][j])
                        self.col_indxs.append(j)
        # from 3 arrays

        elif isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            self.items = init_matrix_representation[2]
            self.col_indxs = init_matrix_representation[1]
            self.amounts = [0]
            cur_sum = 0
            prev = init_matrix_representation[0][0]
            for i in range(len(init_matrix_representation[0])):
                if init_matrix_representation[0][i] != prev:
                    prev = init_matrix_representation[0][i]
                    self.amounts.append(cur_sum + self.amounts[-1])
                    cur_sum = 0
                else:
                    cur_sum += 1
        else:
            raise ValueError

    def __getitem__(self, index):
        if (index[0] > len(self.amounts)) or (index[1] > max(self.col_indxs) + 1):
            raise ValueError
        for i in range(self.amounts[index[0]] - self.amounts[index[0]-1]):
            if self.col_indxs[self.amounts[index[0]-1] + i] == index[1] - 1:
                return self.items[self.amounts[index[0]-1] + i]
        return 0

    def __setitem__(self, key, value):
        if (key[0] > len(self.amounts)) or (key[1] > max(self.col_indxs) + 1):
            raise ValueError
        for i in range(self.amounts[key[0]] - self.amounts[key[0]-1]):
            if self.col_indxs[self.amounts[key[0]-1] + i] == key[1] - 1:
                self.items[self.amounts[key[0] - 1] + i] = value
                return
        self.items.insert(self.amounts[key[0] - 1], value)
        self.col_indxs.insert(self.amounts[key[0] - 1], key[1])
        for k in range(len(self.amounts) - key[0]):
            self.amounts[-k-1] += 1

    def __add__(self, other):
        if (len(self.amounts) != len(other.amounts)) or (max(self.col_indxs) != max(other.col_indxs)):
            raise ValueError
	a = []
        out = CSRMatrix(a)
        # за один проход,добавляем сначала меньший индекс столбца из self и other,если в одном кончаются пишем все из
        # другого
        for i in range(len(self.amounts) - 1):
            out.amounts.append(out.amounts[-1])
            cur_row_len_s = self.amounts[i+1] - self.amounts[i]
            cur_row_len_o = other.amounts[i+1] - other.amounts[i]
            cur_pos_s = self.amounts[i] + 1
            cur_pos_o = other.amounts[i] + 1

            while cur_row_len_s + cur_row_len_o > 0:
                if (cur_row_len_s > 0) and (cur_row_len_o > 0):
                    if self.col_indxs[cur_pos_s - 1] < other.col_indxs[cur_pos_o - 1]:
                        out.items.append(self.items[cur_pos_s-1])
                        out.col_indxs.append(self.col_indxs[cur_pos_s-1])
                        out.amounts[-1] += 1
                        cur_pos_s += 1
                        cur_row_len_s -= 1

                    elif self.col_indxs[cur_pos_s - 1] == other.col_indxs[cur_pos_o - 1]:
                        if self.items[cur_pos_s - 1] + other.items[cur_pos_o - 1] != 0:
                            out.items.append(self.items[cur_pos_s - 1] + other.items[cur_pos_o - 1])
                            out.col_indxs.append(self.col_indxs[cur_pos_s - 1])
                            out.amounts[-1] += 1
                        cur_pos_s += 1
                        cur_pos_o += 1
                        cur_row_len_s -= 1
                        cur_row_len_o -= 1

                    elif self.col_indxs[cur_pos_s-1] > other.col_indxs[cur_pos_o - 1]:
                        out.items.append(other.items[cur_pos_o - 1])
                        out.col_indxs.append(other.col_indxs[cur_pos_o - 1])
                        out.amounts[-1] += 1
                        cur_pos_o += 1
                        cur_row_len_o -= 1

                elif (cur_row_len_s > 0) and (cur_row_len_o == 0):
                    out.items.append(self.items[cur_pos_s - 1])
                    out.col_indxs.append(self.col_indxs[cur_pos_s - 1])
                    out.amounts[-1] += 1
                    cur_pos_s += 1
                    cur_row_len_s -= 1

                elif (cur_row_len_s == 0) and (cur_row_len_o > 0):
                    out.items.append(other.items[cur_pos_o - 1])
                    out.col_indxs.append(other.col_indxs[cur_pos_o - 1])
                    out.amounts[-1] += 1
                    cur_pos_o += 1
                    cur_row_len_o -= 1

        return out

    def __sub__(self, other):
        if (len(self.amounts) != len(other.amounts)) or (max(self.col_indxs) != max(other.col_indxs)):
            raise ValueError
        a = []
        out = CSRMatrix(a)
        for i in range(len(self.amounts) - 1):
            out.amounts.append(out.amounts[-1])
            cur_row_len_s = self.amounts[i+1] - self.amounts[i]
            cur_row_len_o = other.amounts[i+1] - other.amounts[i]
            cur_pos_s = self.amounts[i] + 1
            cur_pos_o = other.amounts[i] + 1

            while cur_row_len_s + cur_row_len_o > 0:
                if (cur_row_len_s > 0) and (cur_row_len_o > 0):
                    if self.col_indxs[cur_pos_s - 1] < other.col_indxs[cur_pos_o - 1]:
                        out.items.append(self.items[cur_pos_s-1])
                        out.col_indxs.append(self.col_indxs[cur_pos_s-1])
                        out.amounts[-1] += 1
                        cur_pos_s += 1
                        cur_row_len_s -= 1

                    elif self.col_indxs[cur_pos_s - 1] == other.col_indxs[cur_pos_o - 1]:
                        if self.items[cur_pos_s - 1] + other.items[cur_pos_o - 1] != 0:
                            out.items.append(self.items[cur_pos_s - 1] - other.items[cur_pos_o - 1])
                            out.col_indxs.append(self.col_indxs[cur_pos_s-1])
                            out.amounts[-1] += 1
                        cur_pos_s += 1
                        cur_pos_o += 1
                        cur_row_len_s -= 1
                        cur_row_len_o -= 1

                    elif self.col_indxs[cur_pos_s-1] > other.col_indxs[cur_pos_o - 1]:
                        out.items.append(- other.items[cur_pos_o - 1])
                        out.col_indxs.append(other.col_indxs[cur_pos_o - 1])
                        out.amounts[-1] += 1
                        cur_pos_o += 1
                        cur_row_len_o -= 1

                elif (cur_row_len_s > 0) and (cur_row_len_o == 0):
                    out.items.append(self.items[cur_pos_s - 1])
                    out.col_indxs.append(self.col_indxs[cur_pos_s - 1])
                    out.amounts[-1] += 1
                    cur_pos_s += 1
                    cur_row_len_s -= 1

                elif (cur_row_len_s == 0) and (cur_row_len_o > 0):
                    out.items.append(- other.items[cur_pos_o - 1])
                    out.col_indxs.append(other.col_indxs[cur_pos_o - 1])
                    out.amounts[-1] += 1
                    cur_pos_o += 1
                    cur_row_len_o -= 1

        return out

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            if other == 0:
		a = []
                out = CSRMatrix(a)
                out.amounts = [0]*len(self.amounts)
                return out
            out = copy.deepcopy(self)
            for i in range(len(self.items)):
                out.items[i] = self.items[i] * other
            return out

        if (len(self.amounts) != len(other.amounts)) or (max(self.col_indxs) != max(other.col_indxs)):
            raise ValueError
        a = []
        out = CSRMatrix(a)
        for i in range(len(self.amounts) - 1):
            out.amounts.append(out.amounts[-1])
            for dif_c in range(self.amounts[i + 1] - self.amounts[i]):  # amount of items in i row of self
                if self.col_indxs[self.amounts[i] + dif_c] in other.col_indxs[other.amounts[i]:other.amounts[i + 1]]:
                    vr = self.col_indxs[self.amounts[i] + dif_c]
                    o_d = other.col_indxs[other.amounts[i]:other.amounts[i + 1]].index(vr)
                    out.items.append(self.items[self.amounts[i] + dif_c] * other.items[other.amounts[i] + o_d])
                    out.col_indxs.append(self.col_indxs[self.amounts[i] + dif_c])
                    out.amounts[-1] += 1
        return out

    def __truediv__(self, other):
        if other == 0:
            raise ValueError
        out = copy.deepcopy(self)
        for i in range(len(self.items)):
            out.items[i] = self.items[i] / other
        return out

    def transp(self):
	a = []
        out = CSRMatrix(a)
        m = max(self.col_indxs)
        for col_n in range(m+1):
            out.amounts.append(out.amounts[-1])
            for row_n in range(len(self.amounts) - 1):
                if col_n in self.col_indxs[self.amounts[row_n]:self.amounts[row_n + 1]]:
                    inx = self.col_indxs[self.amounts[row_n]:self.amounts[row_n + 1]].index(col_n) + self.amounts[row_n]
                    out.items.append(self.items[inx])
                    out.amounts[-1] += 1
                    out.col_indxs.append(row_n)
        return out

    def __matmul__(self, other):
        if max(self.col_indxs)+1 != len(other.amounts) - 1:
            raise ValueError
	a = []
        out = CSRMatrix(a)
        matr = other.transp()

        for row_n in range(len(self.amounts) - 1):  # go by rows at first matrix
            out.amounts.append(out.amounts[-1])
            for col_n in range(len(matr.amounts) - 1):  # go by colons at second matrix
                sm = 0
                for el_ind in range(self.amounts[row_n], self.amounts[row_n + 1]):  # check row items
                    if self.col_indxs[el_ind] in matr.col_indxs[matr.amounts[col_n]:matr.amounts[col_n+1]]:
                        inx = matr.col_indxs[matr.amounts[col_n]:matr.amounts[col_n + 1]].index(self.col_indxs[el_ind])
                        sm += self.items[el_ind] * matr.items[matr.amounts[col_n] + inx]
                out.items.append(sm)
                out.amounts[-1] += 1
                out.col_indxs.append(col_n)
        return out

    def dot(self, other):
        return self.__matmul__(other)

    def to_dense(self):
        if len(self.items) == 0:
            return None
        row_amount = len(self.amounts) - 1
        col_amount = max(self.col_indxs) + 1
        dense = []
        for i in range(row_amount):
            dense.append([0] * col_amount)
        for row_cnt in range(row_amount):
            for i_ct in range(self.amounts[row_cnt + 1]-self.amounts[row_cnt]):
                dense[row_cnt][self.col_indxs[self.amounts[row_cnt] + i_ct]] = self.items[self.amounts[row_cnt] + i_ct]
        return dense
