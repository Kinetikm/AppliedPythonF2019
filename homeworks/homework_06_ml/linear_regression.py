import numpy as np


class LinearRegression:
    def __init__(self, batch_size=50, max_iter=1000, regr=False):
        self.batch_size = batch_size
        self.max_iter = max_iter
        # in depends on regression choose loss function and it's gradient
        if regr:
            self.lambda_coef = 10**-3
            self.loss = self.__elastic_func
            self.grad_loss = self.__grad_elastic_func
        else:
            self.lambda_coef = 10**-1
            self.loss = self.__mae_func
            self.grad_loss = self.__grad_mae_func

    def __mae_func(self, X, y):
        return np.mean(np.abs(self.predict(X) - y))

    def __grad_mae_func(self, X, y):
        grad = np.zeros(len(self.weights))
        sign = np.sign(self.predict(X) - y)
        grad[0] = np.mean(sign)
        grad[1:] = np.mean(X*sign[:, None], axis=0)
        return grad

    def __elastic_func(self, X, y, lambda1=1, lambda2=1):
        return (np.linalg.norm(self.predict(X) - y)**2 +
                lambda1 * np.sum(np.abs(self.weights)) +
                lambda2 * np.linalg.norm(self.weights)**2)

    def __grad_elastic_func(self, X, y, lambda1=1, lambda2=1):
        grad = np.zeros(len(self.weights))
        diff = self.predict(X) - y
        grad[0] = (2*np.sum(diff) +
                   lambda1 * np.sign(self.weights[0]) +
                   lambda2 * 2 * self.weights[0])
        grad[1:] = (2*np.sum(X*diff[:, None], axis=0) +
                    lambda1 * np.sign(self.weights)[1:] +
                    lambda2 * 2 * self.weights[1:])
        return grad

    def moving_averange(self, vect, ma_past, gamma=0.9):
        return gamma * ma_past + (1 - gamma) * np.linalg.norm(vect)**2

    def root_mean_square(self, ma, epsilon=0.1):
        return np.sqrt(ma + epsilon)

    def fit(self, X_train, y_train):
        if len(X_train.shape) == 1:
            X_train = np.reshape(X_train, (-1, 1))
        n, m = X_train.shape
        # create zero iteration
        self.weights = np.random.normal(0, 1, m + 1)
        ma_g = 0
        ma_dw = 0
        rms_dw = self.root_mean_square(ma_dw)
        # start the iteration process
        for i in range(self.max_iter):
            for j in np.arange(0, n, self.batch_size):
                # choose part of the training sample
                X_train_part = X_train[j:j + self.batch_size]
                y_train_part = y_train[j:j + self.batch_size]
                # update RMS[g]
                g = self.grad_loss(X_train_part, y_train_part)
                ma_g = self.moving_averange(g, ma_g)
                rms_g = self.root_mean_square(ma_g)
                # update weights
                delta_weights = -rms_dw / rms_g * g
                self.weights += self.lambda_coef*delta_weights
                # update RMS[grad(weights)]
                ma_dw = self.moving_averange(delta_weights, ma_dw)
                rms_dw = self.root_mean_square(ma_dw)

    def predict(self, X):
        return X @ self.weights[1:] + self.weights[0]

    def get_weights(self):
        return self.weights
