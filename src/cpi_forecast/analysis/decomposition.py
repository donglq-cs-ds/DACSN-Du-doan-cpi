"""Bóc tách xu hướng và mùa vụ."""
import numpy as np


def moving_average_trend(y: np.ndarray, window: int = 12) -> np.ndarray:
    """Ước lượng xu hướng bằng trung bình trượt."""
    raise NotImplementedError


def seasonal_component(y: np.ndarray, period: int = 12) -> np.ndarray:
    """Ước lượng thành phần mùa vụ."""
    raise NotImplementedError
