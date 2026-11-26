"""Naive: dự báo bằng giá trị quan sát cuối cùng."""
import numpy as np

from .base import Forecaster


class NaiveForecaster(Forecaster):
    def fit(self, y):
        y = np.asarray(y, dtype=float)
        self.last_ = y[-1]         # phần tử cuối cùng của y
        return self

    def predict(self, h):
        return np.full(h, self.last_)   # tạo mảng gồm h giá trị last_