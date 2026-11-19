"""Kiểm thử loader: dữ liệu gộp phải đủ, liên tục, đúng mốc đóng băng."""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from cpi_forecast.data.loader import FREEZE_DATE, load_cpi_monthly  # noqa: E402


def _load():
    return load_cpi_monthly(
        xlsx_path=ROOT / "data/raw/cpi_2006_2025.xlsx",
        csv_path=ROOT / "data/raw/cpi_2026_bo_sung.csv",
    )


def test_so_dong_du_250():
    assert len(_load()) == 250  # 20 năm x 12 tháng + 10 tháng của 2026


def test_moc_dau_va_moc_cuoi():
    df = _load()
    assert df["date"].iloc[0] == pd.Timestamp("2006-01-01")
    assert df["date"].iloc[-1] == pd.Timestamp(FREEZE_DATE + "-01")


def test_lien_tuc_moi_thang_mot_dong():
    df = _load()
    expected = pd.date_range("2006-01-01", FREEZE_DATE + "-01", freq="MS")
    assert list(df["date"]) == list(expected)


def test_khong_thieu_va_trong_khoang_hop_ly():
    df = _load()
    assert df["mom"].notna().all()
    assert df["mom"].between(97, 105).all()


def test_gia_tri_mau():
    df = _load().set_index("date")["mom"]
    assert df[pd.Timestamp("2006-01-01")] == 101.2
    assert df[pd.Timestamp("2025-12-01")] == 100.19
    assert df[pd.Timestamp("2026-10-01")] == 100.20
