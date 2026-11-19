"""Kiểm tra chất lượng và dựng chuỗi chỉ số CPI từ tỷ lệ thay đổi theo tháng.

Đầu vào (từ loader.load_cpi_monthly): cột date, mom
  mom = CPI so với tháng trước (tháng trước = 100), ví dụ 100.05.

Đầu ra (clean_cpi): thêm 2 cột
  pct   = mom - 100            -> % thay đổi so với tháng trước
  index = chỉ số liên tục, mốc BASE_PERIOD = 100 (mặc định 2006-01)

Dựng chỉ số bằng cách nhân dồn:  I_t = I_(t-1) * mom_t / 100
"""
from pathlib import Path

import pandas as pd

BASE_PERIOD = "2006-01"   # tháng đầu chuỗi được chọn làm kỳ gốc = 100
VALID_RANGE = (97.0, 105.0)  # khoảng hợp lý của mom; ngoài khoảng này nghi lỗi nhập
DEFAULT_OUT = Path("data/processed/cpi_monthly_clean.csv")


def check_quality(df: pd.DataFrame, freeze: str = "2026-10") -> list[str]:
    """Trả về danh sách vấn đề chất lượng (rỗng nghĩa là dữ liệu sạch)."""
    issues = []

    if df["mom"].isna().any():
        months = df.loc[df["mom"].isna(), "date"].dt.strftime("%Y-%m").tolist()
        issues.append(f"Thiếu giá trị mom ở: {months}")

    if df["date"].duplicated().any():
        issues.append("Có tháng bị trùng.")

    if not df["date"].is_monotonic_increasing:
        issues.append("Dữ liệu chưa sắp theo thời gian tăng dần.")

    expected = pd.date_range(df["date"].min(), df["date"].max(), freq="MS")
    missing = expected.difference(df["date"])
    if len(missing) > 0:
        issues.append(f"Thiếu tháng: {missing.strftime('%Y-%m').tolist()}")

    if df["date"].max() > pd.Period(freeze, freq="M").to_timestamp():
        issues.append(f"Có dữ liệu sau mốc đóng băng {freeze}.")

    lo, hi = VALID_RANGE
    out = df[(df["mom"] < lo) | (df["mom"] > hi)]
    if not out.empty:
        issues.append(f"mom ngoài khoảng [{lo}, {hi}]: "
                      f"{out['date'].dt.strftime('%Y-%m').tolist()}")
    return issues


def build_index(mom: pd.Series, base_value: float = 100.0) -> pd.Series:
    """Dựng chỉ số liên tục từ mom; quan sát đầu tiên được đặt = base_value.

    I_1 = base_value;  I_t = I_(t-1) * mom_t / 100  với t >= 2.
    """
    factors = (mom / 100.0).copy()
    factors.iloc[0] = 1.0  # tháng đầu là kỳ gốc: không nhân thêm hệ số nào
    return base_value * factors.cumprod()


def rebase(index: pd.Series, dates: pd.Series, base_period: str) -> pd.Series:
    """Đổi kỳ gốc: chia cho giá trị tại base_period rồi nhân 100."""
    base_date = pd.Period(base_period, freq="M").to_timestamp()
    base_val = index[dates == base_date].iloc[0]
    return index / base_val * 100.0


def clean_cpi(df: pd.DataFrame, freeze: str = "2026-10") -> pd.DataFrame:
    """Kiểm tra chất lượng rồi thêm cột pct và index. Báo lỗi nếu dữ liệu không sạch."""
    issues = check_quality(df, freeze)
    if issues:
        raise ValueError("Dữ liệu chưa sạch:\n- " + "\n- ".join(issues))

    out = df.sort_values("date").reset_index(drop=True).copy()
    out["pct"] = out["mom"] - 100.0
    out["index"] = build_index(out["mom"])
    return out


def run_cleaning(save_path=DEFAULT_OUT) -> pd.DataFrame:
    """Đọc -> làm sạch -> lưu data/processed/cpi_monthly_clean.csv."""
    from cpi_forecast.data.loader import load_cpi_monthly

    clean = clean_cpi(load_cpi_monthly())
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(save_path, index=False, float_format="%.6f")
    return clean


if __name__ == "__main__":
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[2]))
    df = run_cleaning()
    print(f"Đã lưu {len(df)} dòng vào {DEFAULT_OUT}")
    print(df.head(3).to_string(index=False))
    print(df.tail(3).to_string(index=False))