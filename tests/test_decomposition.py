"""Kiểm thử bóc tách xu hướng và mùa vụ."""
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from cpi_forecast.analysis.decomposition import (  # noqa: E402
    decompose,
    moving_average_trend,
    seasonal_component,
)


def test_xu_huong_cua_duong_thang_la_chinh_no():
    y = 2.0 * np.arange(1.0, 41.0)
    trend = moving_average_trend(y, 12)
    assert np.allclose(trend[6:-6], y[6:-6])  # phần giữa chuỗi khớp hoàn toàn
    assert np.isnan(trend[:6]).all() and np.isnan(trend[-6:]).all()


def test_mua_vu_khoi_phuc_mau_lap():
    pattern = np.array([1.0, -1.0, 2.0, -2.0])
    y = np.tile(pattern, 10)  # chuỗi chỉ có mùa vụ chu kỳ 4, không xu hướng
    s = seasonal_component(y, period=4)
    assert np.allclose(s, y)


def test_ba_thanh_phan_cong_lai_bang_chuoi_goc():
    rng = np.random.default_rng(0)
    y = np.arange(60.0) + np.tile([3.0, 0.0, -3.0, 0.0], 15) + rng.normal(0, 0.1, 60)
    d = decompose(y, period=4)
    ok = ~np.isnan(d["xu_huong"])
    assert np.allclose((d["xu_huong"] + d["mua_vu"] + d["con_lai"])[ok], y[ok])