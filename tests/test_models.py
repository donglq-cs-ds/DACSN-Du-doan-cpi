import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from cpi_forecast.models.naive import NaiveForecaster  # noqa: E402
from cpi_forecast.models.seasonal_naive import SeasonalNaiveForecaster  # noqa: E402
from cpi_forecast.models.moving_average import MovingAverageForecaster  # noqa: E402
from cpi_forecast.models.trend_ols import TrendOLSForecaster  # noqa: E402



def test_naive_lap_lai_gia_tri_cuoi():
    model = NaiveForecaster().fit(np.array([100.0, 102.0, 105.0]))
    assert list(model.predict(3)) == [105.0, 105.0, 105.0]

def test_seasonal_naive_lap_lai_nam_truoc():
    y = np.arange(1.0, 25.0)          # chuỗi 1, 2, ..., 24
    model = SeasonalNaiveForecaster(period=12).fit(y)
    # 12 giá trị cuối là 13..24, nên dự báo 3 tháng tới là 13, 14, 15
    assert list(model.predict(3)) == [13.0, 14.0, 15.0]

def test_trung_binh_truot_lay_tb_k_cuoi():
    y = np.array([10.0, 20.0, 30.0, 40.0])
    model = MovingAverageForecaster(k=2).fit(y)
    # trung bình 2 giá trị cuối: (30 + 40) / 2 = 35
    assert list(model.predict(3)) == [35.0, 35.0, 35.0]


def test_ols_duong_thang_hoan_hao():
    y = np.array([2.0, 4.0, 6.0])      # y = 2t, đúng ví dụ tính tay ở trên
    model = TrendOLSForecaster().fit(y)
    assert np.allclose(model.predict(2), [8.0, 10.0])