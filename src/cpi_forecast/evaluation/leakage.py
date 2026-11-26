"""Thí nghiệm rò rỉ dữ liệu: chuẩn hóa (z-score) bằng thống kê của TOÀN chuỗi.

Cách ĐÚNG : tại mỗi mốc, chỉ dùng trung bình và độ lệch chuẩn của dữ liệu
            TRƯỚC mốc đó (đúng thứ tự thời gian).
Cách SAI  : dùng trung bình và độ lệch chuẩn của TOÀN chuỗi, tức là đã
            "nhìn trước" cả phần tương lai (rò rỉ dữ liệu).

Hàm trả về hai con số để so sánh:
  - MAE theo đơn vị chuẩn hóa (z)  : thứ mà người ta hay báo cáo sau khi chuẩn hóa
  - MAE theo đơn vị gốc            : sai số thật của dự báo
"""
import numpy as np


def rolling_origin_zscore(y, model_factory, h=1, leaky=False, min_train=60):
    """Rolling-origin có chuẩn hóa. Trả về (MAE_chuẩn_hóa, MAE_gốc)."""
    y = np.asarray(y, dtype=float)
    mu_all, sd_all = y.mean(), y.std()  # thống kê toàn chuỗi (chỉ dùng khi leaky=True)

    err_z, err_goc = [], []
    for origin in range(min_train, len(y) - h + 1):
        train = y[:origin]
        if leaky:
            mu, sd = mu_all, sd_all           # SAI: có cả tương lai
        else:
            mu, sd = train.mean(), train.std()  # ĐÚNG: chỉ quá khứ

        model = model_factory().fit((train - mu) / sd)
        pred_z = model.predict(h)[-1]            # dự báo theo đơn vị chuẩn hóa
        actual = y[origin + h - 1]

        err_z.append((actual - mu) / sd - pred_z)    # sai số theo đơn vị z
        err_goc.append(actual - (pred_z * sd + mu))  # đổi về đơn vị gốc
    return np.mean(np.abs(err_z)), np.mean(np.abs(err_goc))