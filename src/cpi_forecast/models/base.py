"""Lớp cơ sở chung cho mọi mô hình dự báo."""
import numpy as np


class Forecaster:
    """Giao diện thống nhất: fit() rồi predict(h)."""

    def fit(self, y: np.ndarray) -> "Forecaster":
        raise NotImplementedError

    def predict(self, h: int) -> np.ndarray:
        """Dự báo h bước tiếp theo."""
        raise NotImplementedError
