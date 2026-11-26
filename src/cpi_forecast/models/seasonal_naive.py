"""Seasonal Naive: dự báo bằng giá trị cùng tháng của năm trước."""
import numpy as np

from .base import Forecaster


class SeasonalNaiveForecaster(Forecaster):
    def __init__(self, period=12):
        self.period = period

    def fit(self, y):
        y = np.asarray(y, dtype=float)
        self.season_ = y[-self.period:]        # period phần tử cuối cùng của y
        return self

    def predict(self, h):
        idx = np.arange(h) % self.period    # 0, 1, ..., 11, 0, 1, ... (quay vòng)
        return self.season_[idx]