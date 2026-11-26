"""Hồi quy xu hướng: y_t = b0 + b1 * t, ước lượng OLS bằng phương trình chuẩn."""
import numpy as np

from .base import Forecaster


class TrendOLSForecaster(Forecaster):
    def fit(self, y):
        y = np.asarray(y, dtype=float)
        self.n_ = len(y)
        t = np.arange(1, self.n_ + 1)
        X = np.column_stack([np.ones(self.n_), t])   # cột toàn số 1 và cột t
        # giải (X^T X) b = X^T y
        self.coef_ = np.linalg.solve(X.T @ X, X.T @ y)
        return self

    def predict(self, h):
        t_future = np.arange(self.n_ + 1, self.n_ + h + 1)   # các tháng tiếp theo
        return self.coef_[0] + self.coef_[1] * t_future                    # b0 + b1 * t