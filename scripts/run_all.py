"""Chạy trọn quy trình từ dữ liệu gốc đến kết quả.

    python scripts/run_all.py

Các bước:
  1. Làm sạch dữ liệu          -> data/processed/cpi_monthly_clean.csv
  2. Đánh giá rolling-origin   -> results/tables/rolling_origin_*.csv
  3. Chẩn đoán sai số (h = 1)  -> results/tables/diagnostics_*.csv
  4. Thí nghiệm rò rỉ dữ liệu  -> results/tables/leakage.csv
  5. Bóc tách xu hướng, mùa vụ -> results/tables/seasonal_profile_pct.csv
  6. Vẽ hình cho báo cáo       -> results/figures/*.png
"""
import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # vẽ ra file, không cần mở cửa sổ
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Chạy được từ bất kỳ thư mục nào: đưa về thư mục gốc dự án.
ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / "src"))

from cpi_forecast.analysis.decomposition import decompose  # noqa: E402
from cpi_forecast.data.cleaning import run_cleaning  # noqa: E402
from cpi_forecast.evaluation.diagnostics import (  # noqa: E402
    autocorrelation,
    residual_summary,
    rolling_origin_errors,
)
from cpi_forecast.evaluation.leakage import rolling_origin_zscore  # noqa: E402
from cpi_forecast.evaluation.rolling_origin import rolling_origin_eval  # noqa: E402
from cpi_forecast.models.moving_average import MovingAverageForecaster  # noqa: E402
from cpi_forecast.models.naive import NaiveForecaster  # noqa: E402
from cpi_forecast.models.seasonal_naive import SeasonalNaiveForecaster  # noqa: E402
from cpi_forecast.models.trend_ols import TrendOLSForecaster  # noqa: E402

TABLES = Path("results/tables")
FIGURES = Path("results/figures")
HORIZONS = (1, 3, 6)
MIN_TRAIN = 60

MODELS = {
    "Naive": NaiveForecaster,
    "Seasonal Naive": SeasonalNaiveForecaster,
    "Trung bình trượt (k=3)": lambda: MovingAverageForecaster(k=3),
    "Hồi quy xu hướng (OLS)": TrendOLSForecaster,
}
SERIES = {"index": "index", "pct": "pct"}


def step_evaluate(df):
    for col in SERIES:
        rows = []
        for name, factory in MODELS.items():
            # MAPE chia cho 0 ở chuỗi pct (có tháng bằng 0) -> inf; đã biết, bỏ cảnh báo
            with np.errstate(divide="ignore", invalid="ignore"):
                res = rolling_origin_eval(df[col].to_numpy(), factory, HORIZONS, MIN_TRAIN)
            row = {"Mô hình": name}
            for h, (mae_v, mape_v) in res.items():
                row[f"MAE h={h}"] = round(mae_v, 3)
                row[f"MAPE h={h}"] = round(mape_v, 3)
            rows.append(row)
        table = pd.DataFrame(rows)
        table.to_csv(TABLES / f"rolling_origin_{col}.csv", index=False)
        print(f"\n  Chuỗi {col}:")
        print(table[["Mô hình", "MAE h=1", "MAE h=3", "MAE h=6"]].to_string(index=False))


def step_diagnostics(df):
    for col in SERIES:
        rows = []
        for name, factory in MODELS.items():
            s = residual_summary(rolling_origin_errors(df[col].to_numpy(), factory, 1, MIN_TRAIN))
            rows.append({"Mô hình": name,
                         "Trung bình sai số": round(s["trung_binh"], 3),
                         "Độ lệch chuẩn": round(s["do_lech_chuan"], 3),
                         "ACF lag 1": round(s["acf_lag1"], 2),
                         "ACF lag 12": round(s["acf_lag12"], 2)})
        pd.DataFrame(rows).to_csv(TABLES / f"diagnostics_{col}.csv", index=False)
    print("  Đã lưu diagnostics_index.csv, diagnostics_pct.csv")


def step_leakage(df):
    rows = []
    for col in SERIES:
        for name, factory in MODELS.items():
            z_ok, g_ok = rolling_origin_zscore(df[col].to_numpy(), factory, 1, False, MIN_TRAIN)
            z_lk, g_lk = rolling_origin_zscore(df[col].to_numpy(), factory, 1, True, MIN_TRAIN)
            rows.append({"Chuỗi": col, "Mô hình": name,
                         "MAE chuẩn hóa (đúng)": round(z_ok, 3),
                         "MAE chuẩn hóa (rò rỉ)": round(z_lk, 3),
                         "Tỉ lệ rò rỉ/đúng": round(z_lk / z_ok, 2),
                         "MAE gốc (đúng)": round(g_ok, 3),
                         "MAE gốc (rò rỉ)": round(g_lk, 3)})
    pd.DataFrame(rows).to_csv(TABLES / "leakage.csv", index=False)
    print("  Đã lưu leakage.csv")


def step_decomposition(df):
    d = decompose(df["pct"].to_numpy(), period=12)
    profile = pd.DataFrame({"Tháng": [f"T{k}" for k in range(1, 13)],
                            "Chỉ số mùa vụ (điểm %)": d["mua_vu"][:12].round(2)})
    profile.to_csv(TABLES / "seasonal_profile_pct.csv", index=False)
    print("  Đã lưu seasonal_profile_pct.csv")
    return d


def step_figures(df, d):
    # 1. Hai chuỗi
    fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    ax[0].plot(df["date"], df["index"]); ax[0].set_title("Chỉ số CPI (01/2006 = 100)")
    ax[1].plot(df["date"], df["pct"]); ax[1].axhline(0, color="gray", linewidth=0.8)
    ax[1].set_title("% thay đổi so với tháng trước")
    fig.tight_layout(); fig.savefig(FIGURES / "01_hai_chuoi.png", dpi=150); plt.close(fig)

    # 2. Bóc tách
    fig, ax = plt.subplots(4, 1, figsize=(10, 9), sharex=True)
    ax[0].plot(df["date"], df["pct"]); ax[0].set_title("% thay đổi (chuỗi gốc)")
    ax[1].plot(df["date"], d["xu_huong"]); ax[1].set_title("Xu hướng (trung bình trượt 12 tháng)")
    ax[2].plot(df["date"], d["mua_vu"]); ax[2].set_title("Mùa vụ")
    ax[3].plot(df["date"], d["con_lai"]); ax[3].set_title("Phần còn lại")
    fig.tight_layout(); fig.savefig(FIGURES / "02_boc_tach_pct.png", dpi=150); plt.close(fig)

    # 3. Chẩn đoán sai số của Naive trên chuỗi chỉ số
    e = rolling_origin_errors(df["index"].to_numpy(), NaiveForecaster, 1, MIN_TRAIN)
    dates = df["date"].iloc[MIN_TRAIN:]
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    ax[0].plot(dates, e); ax[0].axhline(0, color="gray"); ax[0].set_title("Sai số theo thời gian")
    ax[1].hist(e, bins=25); ax[1].set_title("Phân phối sai số")
    band = 1.96 / np.sqrt(len(e))
    ax[2].bar(range(1, 13), autocorrelation(e, 12))
    ax[2].axhline(band, ls="--", color="red"); ax[2].axhline(-band, ls="--", color="red")
    ax[2].set_title("Tự tương quan (ACF)")
    fig.tight_layout(); fig.savefig(FIGURES / "03_chan_doan_naive_index.png", dpi=150); plt.close(fig)
    print("  Đã lưu 3 hình vào results/figures/")


def main():
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    print("[1/6] Làm sạch dữ liệu")
    clean = run_cleaning()
    df = clean.copy()
    print(f"  {len(df)} dòng, {df['date'].min():%m/%Y} đến {df['date'].max():%m/%Y}")

    print("\n[2/6] Đánh giá rolling-origin (MAE; MAPE xem trong file CSV)")
    step_evaluate(df)

    print("\n[3/6] Chẩn đoán sai số (tầm 1 tháng)")
    step_diagnostics(df)

    print("\n[4/6] Thí nghiệm rò rỉ dữ liệu")
    step_leakage(df)

    print("\n[5/6] Bóc tách xu hướng và mùa vụ")
    d = step_decomposition(df)

    print("\n[6/6] Vẽ hình")
    step_figures(df, d)

    print("\nXong. Kết quả nằm trong data/processed, results/tables, results/figures.")


if __name__ == "__main__":
    main()