#!/usr/bin/env python
# coding: utf-8


import numpy as np
from sklearn.metrics import log_loss, mean_squared_error, mean_absolute_error


class Tree:
    def __init__(self, criterion, max_depth, min_samples_leaf=1):
        '''
                Объявляем переменные класса.
        '''

        self.max_depth = max_depth  # максимальная глубина
        self.min_size = 1  # минимальный размер поддерева
        self.value = 0  # значение в поддереве (среднее по всем листьям)
        self.feature_idx = -1  # номер лучшего признака
        self.feature_threshold = 0  # значение лучшего признака
        self.left = None  # левый потомок
        self.right = None  # правый потомок

    def mse(self, y_hat, y):
        mse = (y_hat - y) * (y_hat - y) / y.shape[0]

    def fit(self, X, y):

        '''
        Процедура обучения дерева. На выходе получим обученную модель.
        '''

        # инициализируем начальные значения
        self.value = y.mean()
        base_error = ((y - self.value) ** 2).sum()
        error = base_error
        flag = 0

        # ошибки в левом и правом поддереве
        prev_error_left = base_error
        prev_error_right = 0

        # если дошли до глубины 0 - выходим
        if self.max_depth <= 1:
            return

        dim_shape = X.shape[1]

        # значения в левом и правом поддереве
        left_value = 0
        right_value = 0

        # начинаем цикл по признакам
        for feat in range(dim_shape):

            # сортируем признаки
            idxs = np.argsort(X[:, feat])

            # количество сэмплов в левом и правом поддереве
            N = X.shape[0]
            N1, N2 = N, 0
            thres = 1

            # начинаем проходиться по значениям признака
            while thres < N - 1:
                N1 -= 1
                N2 += 1

                idx = idxs[thres]
                x = X[idx, feat]

                # пропускаем одинаковые признаки
                if thres < N - 1 and x == X[idxs[thres + 1], feat]:
                    thres += 1
                    continue

                # данные, которые получаются у нас в результате такого сплита
                target_right = y[idxs][:thres]
                target_left = y[idxs][thres:]
                mean_right = y[idxs][:thres].mean(),
                mean_left = y[idxs][thres:].mean()

                # на этом шаге уже нужно считать ошибку -
                # генерируем предикты (среднее в потомках)
                left_shape = target_left.shape[0]
                right_shape = target_right.shape[0]
                mean_left_array = [mean_left for _ in range(left_shape)]
                mean_right_array = [mean_right for _ in range(right_shape)]

                # считаем ошибку слева и справа
                prev_error_left = N1 / N * mean_squared_error(target_left, mean_left_array)
                prev_error_right = N2 / N * mean_squared_error(target_right, mean_right_array)

                # если выполняются условия сплита, то обновляем
                if (prev_error_left + prev_error_right < error):
                    if (min(N1, N2) > self.min_size):
                        self.feature_idx = feat
                        self.feature_threshold = x
                        left_value = mean_left
                        right_value = mean_right

                        flag = 1
                        error = prev_error_left + prev_error_right

                thres += 1

        # если не нашли лучший сплит, выходим
        if self.feature_idx == -1:
            return

        # дошли сюда - есть хорошее разбиение, нужно обучать дальше
        # инициализируем потомков - те же деревья решений
        a = self.max_depth - 1
        self.left = TreeRegressor(max_depth=a)
        self.left.value = left_value
        self.right = TreeRegressor(max_depth=a)
        self.right.value = right_value

        # индексы потомков
        idxs_l = (X[:, self.feature_idx] > self.feature_threshold)
        idxs_r = (X[:, self.feature_idx] <= self.feature_threshold)

        # обучаем
        self.left.fit(X[idxs_l, :], y[idxs_l])
        self.right.fit(X[idxs_r, :], y[idxs_r])


class TreeRegressor(Tree):
    def __init__(self, criterion='mse', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'mse' or 'mae'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)

    def __predict(self, x):

        '''
        Функция для генерирования предсказания - смотрим узлы, идем
        в соответствующих  потомков и смотрим в конце self.value - это
        и будет ответом.
        '''

        if self.feature_idx == -1:
            return self.value

        if x[self.feature_idx] > self.feature_threshold:
            return self.left.__predict(x)
        else:
            return self.right.__predict(x)

    def predict(self, X):

        '''
        Предикт для матрицы - просто для каждой строчки вызываем __predict().
        '''

        y = np.zeros(X.shape[0])

        for i in range(X.shape[0]):
            y[i] = self.__predict(X[i])

        return y


class TreeClassifier(Tree):
    def __init__(self, criterion='gini', max_depth=None, min_samples_leaf=1):
        """
        :param criterion: method to determine splits, 'gini' or 'entropy'
        """
        super().__init__(criterion, max_depth, min_samples_leaf)
        raise NotImplementedError
