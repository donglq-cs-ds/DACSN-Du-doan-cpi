"""Bóc tách chuỗi thời gian thành: xu hướng + mùa vụ + phần còn lại.

Mô hình cộng:   y_t = xu_huong_t + mua_vu_t + con_lai_t

Lưu ý: chuỗi phải bắt đầu từ THÁNG 1 (đúng như dữ liệu CPI của ta, 01/2006),
để vị trí 0 trong chuỗi ứng với tháng 1, vị trí 1 ứng với tháng 2, ...
"""
import numpy as np


def moving_average_trend(y, window=12):
    """Ước lượng xu hướng bằng trung bình trượt căn giữa.

    Với window chẵn (12) dùng trung bình trượt "2 x 12": các trọng số
    0,5 / 1 / 1 / ... / 1 / 0,5 (chia 12) để kết quả căn giữa đúng tháng.
    Mỗi đầu chuỗi mất window/2 giá trị (để NaN).
    """
    y = np.asarray(y, dtype=float)
    n = len(y)
    if window % 2 == 0:
        w = np.r_[0.5, np.ones(window - 1), 0.5] / window
    else:
        w = np.ones(window) / window
    k = len(w) // 2
    trend = np.full(n, np.nan)
    trend[k : n - k] = np.convolve(y, w, mode="valid")
    return trend


def seasonal_component(y, period=12):
    """Ước lượng thành phần mùa vụ.

    Bước 1: bỏ xu hướng  ->  y - xu_huong
    Bước 2: với mỗi tháng trong năm (tháng 1, tháng 2, ...) lấy trung bình
            các giá trị đã bỏ xu hướng của tháng đó qua các năm
    Bước 3: trừ đi trung bình chung để tổng 12 chỉ số mùa vụ bằng 0
    """
    y = np.asarray(y, dtype=float)
    detrended = y - moving_average_trend(y, period)
    pos = np.arange(len(y)) % period
    profile = np.array([np.nanmean(detrended[pos == k]) for k in range(period)])
    profile = profile - profile.mean()
    return profile[pos]


def decompose(y, period=12):
    """Trả về dict gồm xu hướng, mùa vụ và phần còn lại."""
    y = np.asarray(y, dtype=float)
    trend = moving_average_trend(y, period)
    seasonal = seasonal_component(y, period)
    return {"xu_huong": trend, "mua_vu": seasonal, "con_lai": y - trend - seasonal}