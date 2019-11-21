#!/usr/bin/env python
# coding: utf-8


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
        raise NotImplementedError

    def fit(self, X_train, y_train):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        pass

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        pass

# создать функцию для средней оценки
# написать алгоритм, который использует градиентный спуск с оптимизацией для обучения базовых алгоритмов 
# Используя написанное ранее дерево: переделать под регрессию!
# создать список базовых алгоритмов, заполнить его константным для MSE
#for i in range(T) # T = n_estimators
#    for j in range(N):
#        