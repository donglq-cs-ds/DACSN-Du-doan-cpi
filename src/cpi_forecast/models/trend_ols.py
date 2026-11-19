"""Hồi quy xu hướng, ước lượng OLS bằng phương trình chuẩn (X'X)b = X'y."""
import numpy as np

from .base import Forecaster


class TrendOLSForecaster(Forecaster):
    def fit(self, y: np.ndarray) -> "TrendOLSForecaster":
        raise NotImplementedError

    def predict(self, h: int) -> np.ndarray:
        raise NotImplementedError
