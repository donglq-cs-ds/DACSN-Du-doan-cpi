"""Trung bình trượt: dự báo bằng trung bình k quan sát gần nhất."""
import numpy as np

from .base import Forecaster


class MovingAverageForecaster(Forecaster):
    def __init__(self, k=3):
        self.k = k

    def fit(self, y):
        y = np.asarray(y, dtype=float)
        self.mean_ = y[-self.k:].mean()          # trung bình của k phần tử cuối của y
        return self

    def predict(self, h):
        return np.full(h, self.mean_)