"""Đọc và gộp dữ liệu CPI hàng tháng của Việt Nam.

Dữ liệu đầu vào đều ở thang "tháng trước = 100" (ví dụ 100.05 nghĩa là
CPI tăng 0,05% so với tháng trước):
  1. Bảng Excel 2006-2025: hàng là tháng, cột là năm (dạng "rộng").
  2. File CSV bổ sung 2026: mỗi dòng một tháng (dạng "dài").

Đầu ra của load_cpi_monthly(): DataFrame có 2 cột
  - date: ngày đầu tháng (datetime64)
  - mom : CPI so với tháng trước (tháng trước = 100)
"""
from pathlib import Path

import pandas as pd

# Mốc "đóng băng" dữ liệu: không dùng quan sát nào sau tháng này.
FREEZE_DATE = "2026-10"

DEFAULT_XLSX = Path("data/raw/cpi_2006_2025.xlsx")
DEFAULT_CSV = Path("data/raw/cpi_2026_bo_sung.csv")


def load_wide_table(path=DEFAULT_XLSX) -> pd.DataFrame:
    """Đọc bảng Excel dạng rộng (hàng = tháng, cột = năm) -> dạng dài.

    Cấu trúc sheet: dòng 1 là tiêu đề, dòng 2 trống, dòng 3 là các năm,
    từ dòng 4 là "Tháng 1" ... "Tháng 12".
    """
    wide = pd.read_excel(path, header=2, index_col=0)

    # Tên cột là năm nhưng đọc ra dạng số thực (2006.0) -> ép về số nguyên.
    wide.columns = wide.columns.astype(float).astype(int)

    # Chỉ giữ các dòng có nhãn dạng "Tháng k".
    wide = wide[wide.index.astype(str).str.match(r"^\s*Tháng\s+\d+\s*$")]

    # Chuyển từ rộng sang dài: mỗi dòng một cặp (tháng, năm).
    long = (
        wide.rename_axis("nhan_thang")
        .reset_index()
        .melt(id_vars="nhan_thang", var_name="nam", value_name="mom")
    )
    long["thang"] = long["nhan_thang"].str.extract(r"(\d+)", expand=False).astype(int)
    long["date"] = pd.to_datetime(
        {"year": long["nam"], "month": long["thang"], "day": 1}
    )
    long["mom"] = pd.to_numeric(long["mom"], errors="coerce")
    return long[["date", "mom"]]


def load_supplement(path=DEFAULT_CSV) -> pd.DataFrame:
    """Đọc file CSV bổ sung (các tháng 2026) -> cùng dạng với load_wide_table."""
    df = pd.read_csv(path)
    out = pd.DataFrame(
        {
            "date": pd.to_datetime(
                {"year": df["nam"], "month": df["thang"], "day": 1}
            ),
            "mom": pd.to_numeric(df["cpi_so_voi_thang_truoc"], errors="coerce"),
        }
    )
    return out


def load_cpi_monthly(
    xlsx_path=DEFAULT_XLSX, csv_path=DEFAULT_CSV, freeze=FREEZE_DATE
) -> pd.DataFrame:
    """Gộp hai nguồn, sắp theo thời gian và cắt cứng tại mốc đóng băng."""
    df = pd.concat([load_wide_table(xlsx_path), load_supplement(csv_path)])

    # Cùng một tháng xuất hiện 2 lần là lỗi dữ liệu -> báo lỗi, không tự bỏ.
    dup = df["date"].duplicated()
    if dup.any():
        raise ValueError(f"Có tháng bị trùng: {df.loc[dup, 'date'].dt.strftime('%Y-%m').tolist()}")

    df = df.sort_values("date")

    # Cắt cứng: giữ các tháng <= freeze (ví dụ 2026-10).
    cutoff = pd.Period(freeze, freq="M").to_timestamp()
    df = df[df["date"] <= cutoff]
    return df.reset_index(drop=True)