"""Kiểm thử chẩn đoán sai số."""
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from cpi_forecast.evaluation.diagnostics import (  # noqa: E402
    autocorrelation,
    residual_summary,
    rolling_origin_errors,
)
from cpi_forecast.models.naive import NaiveForecaster  # noqa: E402


def test_sai_so_naive_chuoi_tang_deu():
    y = np.arange(1.0, 21.0)  # mỗi tháng tăng đúng 1
    e = rolling_origin_errors(y, NaiveForecaster, h=1, min_train=5)
    assert len(e) == 15
    assert np.allclose(e, 1.0)  # Naive luôn thấp hơn thực tế đúng 1


def test_tu_tuong_quan_chuoi_xen_ke():
    e = np.array([1.0, -1.0] * 10)  # +1, -1, +1, -1, ...
    acf = autocorrelation(e, max_lag=2)
    assert np.isclose(acf[0], -0.95)  # liền kề trái dấu -> âm mạnh
    assert np.isclose(acf[1], 0.9)    # cách 2 tháng cùng dấu -> dương mạnh


def test_tom_tat_co_du_khoa():
    s = residual_summary(np.array([1.0, 2.0, 3.0, 2.0, 1.0] * 6))
    assert {"trung_binh", "do_lech_chuan", "acf_lag1", "acf_lag12"} <= set(s)