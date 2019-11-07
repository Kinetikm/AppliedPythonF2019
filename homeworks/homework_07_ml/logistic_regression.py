#!/usr/bin/env python
# coding: utf-8


import numpy as np


# Regularization: l1, Optim: Adam

class LogisticRegression:
    def __init__(self, lambda_coef=0.05, regulatization=None, alpha=0.5, batch_size=100, max_iter=100):
        self.grad_coef = lambda_coef
        self.alpha = alpha
        self.batch = batch_size
        self.iterations = max_iter
        self.weights = np.array(1)

    def fit(self, X_train, y_train):
        X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))  # добавим фиктивный столбец
        beta1 = 0.9
        beta2 = 0.999  # константы для оптимизатора adam
        m_last = 0
        v_last = 0
        eps = 1e-8
        self.weights = np.random.rand(X_train.shape[1])
        for i in range(self.iterations):
            index = np.random.choice(X_train.shape[0], self.batch, replace=False)
            X_batch = X_train[index]
            y_batch = y_train[index]
            y_predict = 1 / (1 + np.exp(-(X_batch @ self.weights)))
            grad = (X_batch.T @ (y_predict - y_batch) + self.alpha * np.sign(self.weights))  # градиент
            m_new = m_last * beta1 + (1 - beta1) * grad
            v_new = v_last * beta2 + (1 - beta2) * (grad * grad)
            m_hat = m_new / (1 - np.power(beta1, i + 1))
            v_hat = v_new / (1 - np.power(beta2, i + 1))
            self.weights -= self.grad_coef * m_hat / np.sqrt(v_hat + eps)
            m_last = m_new
            v_last = v_new

    def predict(self, X_test):
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        y_predict = 1 / (1 + np.exp(-(X_test @ self.weights)))
        for i in range(y_predict.shape[0]):
            if i > 0.5:  # сделал порог ответа равный 0.5
                y_predict[i] = 1
            else:
                y_predict[i] = 0
        return y_predict

    def predict_proba(self, X_test):
        X_test = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
        y_predict = 1 / (1 + np.exp(-(X_test @ self.weights)))
        return y_predict

    def get_weights(self):
        return self.weights
