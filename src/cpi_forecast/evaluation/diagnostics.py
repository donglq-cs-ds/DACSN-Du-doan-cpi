"""Chẩn đoán phần dư của mô hình."""
import numpy as np


def residual_summary(residuals: np.ndarray) -> dict:
    """Trung bình, độ lệch chuẩn, độ lệch/độ nhọn của phần dư."""
    raise NotImplementedError


def autocorrelation(residuals: np.ndarray, max_lag: int = 24) -> np.ndarray:
    """Hàm tự tương quan (ACF) của phần dư."""
    raise NotImplementedError
