"""Seasonal Naive: lặp lại giá trị cùng kỳ năm trước."""
import numpy as np

from .base import Forecaster


class SeasonalNaiveForecaster(Forecaster):
    def fit(self, y: np.ndarray) -> "SeasonalNaiveForecaster":
        raise NotImplementedError

    def predict(self, h: int) -> np.ndarray:
        raise NotImplementedError
