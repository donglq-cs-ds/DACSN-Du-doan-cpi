"""(Mở rộng) Xu hướng + chỉ số mùa vụ."""
import numpy as np

from .base import Forecaster


class TrendSeasonalIndexForecaster(Forecaster):
    def fit(self, y: np.ndarray) -> "TrendSeasonalIndexForecaster":
        raise NotImplementedError

    def predict(self, h: int) -> np.ndarray:
        raise NotImplementedError
