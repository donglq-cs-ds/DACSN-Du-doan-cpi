"""Đánh giá cuốn chiếu (rolling-origin) cho các tầm dự báo 1, 3, 6 tháng."""
import numpy as np

from .metrics import mae, mape


def rolling_origin_eval(y, model_factory, horizons=(1, 3, 6), min_train=60):
    """Trả về {h: (MAE, MAPE)} cho từng tầm dự báo h.

    model_factory: hàm tạo mô hình mới, ví dụ NaiveForecaster
                   hoặc lambda: MovingAverageForecaster(k=3).
    """
    y = np.asarray(y, dtype=float)
    results = {}
    for h in horizons:
        actuals, preds = [], []
        for origin in range(min_train, len(y) - h + 1):
            train = y[:origin]                     # chỉ dữ liệu TRƯỚC mốc: y[:origin]
            model = model_factory()                 # tạo mô hình mới rồi fit(train)
            model.fit(train)
            preds.append(model.predict(h)[-1])  # dự báo của đúng bước thứ h
            actuals.append(y[origin + h - 1])              # giá trị thực ở bước thứ h
        results[h] = (mae(actuals, preds), mape(actuals, preds))
    return results