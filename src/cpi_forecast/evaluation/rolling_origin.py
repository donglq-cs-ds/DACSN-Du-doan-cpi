"""Đánh giá cuốn chiếu (rolling-origin) cho các tầm dự báo 1, 3, 6 tháng."""
import numpy as np

HORIZONS = (1, 3, 6)


def rolling_origin_eval(y: np.ndarray, model_factory, horizons=HORIZONS, min_train: int = 60):
    """Với mỗi mốc gốc: fit trên dữ liệu đến mốc đó, dự báo h bước, tính sai số.

    Trả về dict {h: (mae, mape)} hoặc DataFrame tương đương.
    """
    raise NotImplementedError
