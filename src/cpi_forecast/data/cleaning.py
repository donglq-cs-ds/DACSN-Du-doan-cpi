"""Làm sạch và chuẩn hóa chuỗi CPI."""
import pandas as pd


def standardize_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Chuẩn hóa mốc thời gian về dạng tháng (PeriodIndex/DatetimeIndex)."""
    raise NotImplementedError


def handle_missing_and_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Xử lý giá trị thiếu, dòng trùng, sai định dạng."""
    raise NotImplementedError


def rebase_to_common_base(df: pd.DataFrame, base_period: str) -> pd.DataFrame:
    """Thống nhất năm gốc cho toàn chuỗi."""
    raise NotImplementedError
