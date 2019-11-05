import numpy as np


class LinearRegression:
    def __init__(self, ada_coef=0.9, regularization='L2', alpha=0.5, batch_size=50, max_iter=1000):
        """
        :param regularization: L2
        :param alpha: regularization coefficent
        :param batch_size: num sample per one model parameters update
        :param max_iter: maximum number of parameters updates
        """
        self.ada_coef = ada_coef
        self.alpha = alpha
        self.max_iter = max_iter
        self.batch_size = batch_size
        self.coef_ = None
        self.intercept_ = None

    def normalize(self, x_train):
        return (x_train - np.mean(x_train)) / np.std(x_train)

    def mae(self, x_test, y):
        return sum(abs(np.sum(self.coef_ * x_test, axis=1) - y))

    def grad_func(self, x_train, y_train, coef_last, regulator):
        return -2 * (1 / x_train.shape[0]) * x_train.transpose().dot(y_train) + 2 * (
                1 / x_train.shape[0]) * x_train.transpose().dot(x_train).dot(coef_last) + regulator

    def fit(self, x_train, y_train, eps=1e-5):
        """
        Fit model using gradient descent method
        :param x_train: training data
        :param y_train: target values for training data
        :return: None
        """
        assert x_train.shape[0] == y_train.shape[0], 'Invalid dimensions'
        x_train = self.normalize(x_train)
        x_train = np.hstack([np.ones((x_train.shape[0], 1)), x_train])
        np.random.seed(346346)
        x = np.array_split(x_train, self.batch_size)
        y = np.array_split(y_train, self.batch_size)
        self.coef_ = np.random.randn(x_train.shape[1])
        l2 = 2 * self.alpha * sum(self.coef_)
        tmp_err = np.inf
        indexes = list(range(len(x)))
        np.random.shuffle(indexes)
        sqrs = np.zeros(x_train.shape[1])
        deltas = np.zeros(x_train.shape[1])
        for _ in range(self.max_iter):
            for idx in indexes:
                eps_stable = 1e-8
                g = self.grad_func(x[idx], y[idx], self.coef_, l2) / x[idx].shape[0]
                sqrs = self.ada_coef * sqrs + (1 - self.ada_coef) * np.square(g)
                cur_delta = np.sqrt(deltas + eps_stable) / np.sqrt(sqrs + eps_stable) * g
                deltas = self.ada_coef * deltas + (1 - self.ada_coef) * np.square(cur_delta)
                # update weight
                self.coef_ -= cur_delta
                err = self.mae(x[idx], y[idx])
                if abs(tmp_err - err) / x[idx].shape[0] < eps:
                    return
                tmp_err = err
        self.intercept_ = self.coef_[0]
        self.coef_ = self.coef_[1:]

    def predict(self, x_test):
        assert self.coef_ is not None, 'Model is not fitted'
        return np.sum(self.intercept_ + self.coef_ * x_test, axis=1)

    def get_weights(self):
        assert self.coef_ is not None, 'Model is not fitted'
        return np.hstack((self.intercept_, self.coef_))
