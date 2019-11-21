#!/usr/bin/env python
# coding: utf-8


import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split as tts


class GradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=1.0, max_depth=None,
                 min_samples_leaf=1, subsample=1.0, subsample_col=1.0):
        """
        :param n_estimators: number of trees in model
        :param learning_rate: discount for gradient step
        :param max_depth: maximum depth of tree. If None depth of tree is not constrained
        :param min_samples_leaf: the minimum number of samples required to be at a leaf node
        :param subsample: the fraction of samples to be used for fitting the individual base learners
        :param subsample_col: the fraction of features to be used for fitting the individual base learners
        """
        self.n_estimators = n_estimators
        self.alpha = learning_rate
        self.max_depth = max_depth
        self.min_samles_leaf = min_samples_leaf
        self.subsample = subsample
        self.subsample_col = subsample_col

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        y_train = y_train.reshape(-1, 1)
        N, d = X_train.shape
        self.h_0 = y_train.mean()

        y_step = y_train.copy()
        y_pred = self.h_0

        size = int(d * self.subsample_col)
        self.model = []
        self.feature = []
        for i in range(self.n_estimators):

            y_step -= self.alpha * y_pred

            step_model = DecisionTreeRegressor(
                max_depth=self.max_depth,
                min_samples_leaf=self.min_samles_leaf)

            feature = np.random.choice(d, size)

            X_fit = X_train[:, feature]

            X_n_train, _, y_n_train, _ = tts(
                X_fit, y_step, test_size=1 - self.subsample + 1e-3)
            # Чтобы test_size не было равно 0 если self.subsample равно 1.0

            step_model.fit(X_n_train, y_n_train)

            y_pred = step_model.predict(X_fit).reshape(-1, 1)
            self.feature.append(feature)
            self.model.append(step_model)
        pass

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        res = self.h_0

        for i in range(self.n_estimators):
            res += self.alpha * \
                self.model[i].predict(X_test[:, self.feature[i]]).reshape(-1, 1)
        return res
        pass
