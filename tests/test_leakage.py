"""Kiểm thử thí nghiệm rò rỉ dữ liệu."""
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from cpi_forecast.evaluation.leakage import rolling_origin_zscore  # noqa: E402
from cpi_forecast.models.naive import NaiveForecaster  # noqa: E402


def test_don_vi_goc_khong_doi_nhung_don_vi_chuan_hoa_doi():
    y = np.arange(1.0, 41.0)  # Naive luôn sai đúng 1 đơn vị gốc
    z_ok, g_ok = rolling_origin_zscore(y, NaiveForecaster, h=1, leaky=False, min_train=10)
    z_lk, g_lk = rolling_origin_zscore(y, NaiveForecaster, h=1, leaky=True, min_train=10)
    assert np.isclose(g_ok, 1.0) and np.isclose(g_lk, 1.0)  # sai số thật như nhau
    assert not np.isclose(z_ok, z_lk)                        # nhưng "cây thước" khác nhau