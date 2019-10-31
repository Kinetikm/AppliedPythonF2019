#!/usr/bin/env python
# coding: utf-8
import numpy as np


# Loss: MSE, Regularization: elastic, Optim: NAG

class LinearRegression:
    def __init__(self, lambda_coef=0.005, regulatization='elastic', alpha=0.5, batch_size=50, max_iter=100):
        self.grad_coef = lambda_coef
        self.alpha = alpha
        self.batch = batch_size
        self.iter = max_iter
        self.weights = np.array(1)

    def fit(self, X_train, y_train):
        gamma = 0.1  # коэффициент сохранения
        speed_last = 0
        y_train = y_train[:, np.newaxis]
        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))  # добавляем столбец единиц для свободных весов
        self.weights = np.random.rand(np.shape(X_train)[1], 1)
        for i in range(self.iter):
            np.random.shuffle(X_train)  # на каждой итерации я перемещиваю датасет и беру первый бач,
            predict_f = (X_train[:self.batch] @ self.weights)  # это не оригинальный sgd, но как один из вариантов
            regulariz = self.alpha * np.sign(
                self.weights) + self.alpha * self.weights  # регуляриацию вынес в отдельную
            # переменную
            gradient = X_train[:self.batch].T @ (predict_f - y_train[:self.batch]) + regulariz  # подсчет градиента
            speed_n = gamma * speed_last + self.grad_coef * gradient
            self.weights -= speed_n  # а это как раз оптимизация NAG
            speed_last = speed_n

    def predict(self, X_test):
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        return X_test @ self.weights

    def get_weights(self):
        return self.weights
