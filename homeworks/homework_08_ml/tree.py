#!/usr/bin/env python
# coding: utf-8


import numpy as np


class Tree:
    def __init__(self, criterion, max_depth, min_samples_leaf=1):
        """
        :param criterion: method to determine splits
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        """
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.tree_path = None    # запоминает фичи и пороги, по которым делаем разбиения

    def entropy(self, proba):
        # s = - sum(p_i * log2(p_i)), для бинарного случая i: 0 или 1
        return - proba[0] * np.log2(proba[0]) - proba[1] * np.log2(proba[1])

    def gini(self, proba):
        # g = 1 - sum(p_i ** 2)
        return 1 - (proba[0] ** 2) - (proba[1] ** 2)

    def proba(self, y):
        '''
        p_0 = (кол-во 0) / (общее кол-во таргетов)
        p_1 = (кол-во 1) / (общее кол-во таргетов)
        '''
        return len(y[y == 0]) / len(y), len(y[y == 1]) / len(y)

    def gain(self, s0, y1, y2):
        '''
        gain = s_0 - sum((n_i / n) * s_i)
        s_0 - энтропия либо неопр-ть Джини до разбиения
        s_i - энтропия либо неопр-ть Джини i-й подгруппы
        n_i - количество элементов в i-й подгруппе
        n - количество элементов до разбиения
        '''
        if self.criterion == 'entropy':
            s1 = self.entropy(self.proba(y1))
            s2 = self.entropy(self.proba(y2))
        elif self.criterion == 'gini':
            s1 = self.gini(self.proba(y1))
            s2 = self.gini(self.proba(y2))
        return s0 - (len(y1) * s1 + len(y2) * s2) / (len(y1) + len(y2))

    def build_branch(self, table, depth=0):
        if self.criterion == 'entropy':
            s0 = self.entropy(self.proba(table[:, -1]))
        elif self.criterion == 'gini':
            s0 = self.gini(self.proba(table[:, -1]))
        y_cur = None
        max_gain = 0

        if depth == self.max_depth or table.shape[0] < 2 * self.min_samples_leaf:
            # если количество элементов меньше, чем удвоенное min_samples_leaf, разбить больше не можем
            # если глубина максимальна, возвращаем вероятности 0 и 1 в группе
            return self.proba(table[:, -1])

        for col in range(table.shape[1] - 1):
            # сортируем таблицу по выбранному признаку
            table = np.array(sorted(table, key=lambda x: x[col]))

            # ищем порог, начиная с ряда с номером min_samples_leaf - 1, чтобы в группе не оказалось слишком мало эл-в
            for row in range(self.min_samples_leaf - 1, table.shape[0]):
                # рассматриваем только переходы целевой переменной с 0 на 1 и наоборот
                if y_cur == table[row, -1]:
                    continue
                y_cur = table[row, -1]
                # проверяем, чтобы вторая подгруппа не стала слишком маленькой (не меньше min_samples_leaf)
                if table.shape[0] - row < self.min_samples_leaf:
                    break

                gain = self.gain(s0, table[0:row, -1], table[row:, -1])
                if max_gain < gain:
                    max_gain = gain
                    best_feature = col
                    best_row = row
                    treshold = (table[row, col] + table[row - 1, col]) / 2    # порог - среднее на границе разбиения
                    sorted_table = table

        if max_gain == 0:
            # если максимальный gain == 0, разбивать таблицу не будем
            return self.proba(table[:, -1])
        # нашли оптимальное разбиение, теперь надо разбить полученные подгруппы
        branch1 = self.build_branch(sorted_table[0:best_row], depth=depth + 1)
        branch2 = self.build_branch(sorted_table[best_row:], depth=depth + 1)
        return [(best_feature, treshold), branch1, branch2]

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        # объединяем в одну матрицу, чтобы потом было удобно сортировать по какому-то столбцу
        table = np.append(X_train, np.reshape(y_train, (-1, 1)), axis=1)
        self.tree_path = self.build_branch(table)

    def predicted_value(self, row, path=None):
        if path is None:
            # когда None, начинаем разбиения с самого начала алгоритма
            path = self.tree_path
        if isinstance(path, tuple):
            # если path стал типа tuple, значит мы находимся в листке дерева => возвращаем вероятности в нем
            return path
        # формат path: [tuple со значениями feature и порог, первая ветвь, вторая ветвь], где
        # первая и вторая ветвь - списки такого же формата
        feature = path[0][0]
        treshold = path[0][1]
        if row[feature] <= treshold:
            return self.predicted_value(row, path[1])
        else:
            return self.predicted_value(row, path[2])

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        y_predicted = np.empty(X_test.shape[0])
        for row in X_test:
            np.append(y_predicted, np.argmax(np.array(self.predicted_value(row))))
        return y_predicted

    def get_feature_importance(self):
        """
        Get feature importance from fitted tree
        :return: weights array
        """
        pass


class TreeRegressor(Tree):
    def __init__(self, criterion='mse', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'mse' or 'mae'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)
        raise NotImplementedError


class TreeClassifier(Tree):
    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'gini' or 'entropy'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        y_predicted = np.empty((0, 2))
        for row in X_test:
            preficted_value = np.array(self.predicted_value(row))
            y_predicted = np.append(y_predicted, preficted_value.reshape((1, 2)), axis=0)
        return y_predicted
