import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from cpi_forecast.evaluation.rolling_origin import rolling_origin_eval  # noqa: E402
from cpi_forecast.models.naive import NaiveForecaster  # noqa: E402


def test_rolling_origin_naive_chuoi_tang_deu():
    y = np.arange(1.0, 11.0)   # 1, 2, ..., 10: mỗi tháng tăng đúng 1
    res = rolling_origin_eval(y, NaiveForecaster, horizons=(1, 3), min_train=5)
    # Naive luôn đoán bằng giá trị cuối, nên thấp hơn thực tế đúng h đơn vị
    assert np.isclose(res[1][0], 1.0)   # MAE tầm 1 = 1
    assert np.isclose(res[3][0], 3.0)   # MAE tầm 3 = 3