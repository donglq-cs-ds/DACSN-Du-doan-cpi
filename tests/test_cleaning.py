"""Kiểm thử cleaning: chất lượng dữ liệu và công thức dựng chỉ số."""
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from cpi_forecast.data.cleaning import build_index, check_quality, clean_cpi, rebase  # noqa: E402
from cpi_forecast.data.loader import load_cpi_monthly  # noqa: E402


def _clean():
    raw = load_cpi_monthly(
        xlsx_path=ROOT / "data/raw/cpi_2006_2025.xlsx",
        csv_path=ROOT / "data/raw/cpi_2026_bo_sung.csv",
    )
    return clean_cpi(raw)


def test_chi_so_thang_dau_bang_100():
    assert _clean()["index"].iloc[0] == pytest.approx(100.0)


def test_chi_so_thang_hai_tinh_tay():
    # Tháng 2/2006 có mom = 102.1 -> I = 100 * 1.021 = 102.1
    assert _clean()["index"].iloc[1] == pytest.approx(102.1)


def test_chi_so_nhat_quan_voi_mom():
    df = _clean()
    ratio = df["index"] / df["index"].shift(1) * 100
    assert ratio.iloc[1:].to_numpy() == pytest.approx(df["mom"].iloc[1:].to_numpy())


def test_rebase_ve_100_tai_moc_moi():
    df = _clean()
    new = rebase(df["index"], df["date"], "2015-01")
    assert new[df["date"] == pd.Timestamp("2015-01-01")].iloc[0] == pytest.approx(100.0)


def test_phat_hien_thieu_thang():
    df = _clean().drop(index=100)
    assert any("Thiếu tháng" in s for s in check_quality(df))


def test_phat_hien_gia_tri_la():
    df = _clean()
    df.loc[5, "mom"] = 10.05  # gõ nhầm 100.05 thành 10.05
    assert any("ngoài khoảng" in s for s in check_quality(df))


def test_build_index_vi_du_nho():
    s = pd.Series([101.0, 110.0, 90.0])
    assert build_index(s).tolist() == pytest.approx([100.0, 110.0, 99.0])
