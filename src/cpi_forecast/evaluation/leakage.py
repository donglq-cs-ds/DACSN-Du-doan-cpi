"""Thí nghiệm rò rỉ dữ liệu: chuẩn hóa trên TOÀN chuỗi trước khi chia.

So sánh sai số khi (a) chuẩn hóa đúng (chỉ dùng thống kê của tập train)
với (b) chuẩn hóa sai (dùng thống kê cả chuỗi) để chỉ ra sai số "đẹp giả".
"""
import numpy as np


def standardize_correct(y: np.ndarray, test_size: int):
    raise NotImplementedError


def standardize_leaky(y: np.ndarray, test_size: int):
    raise NotImplementedError
