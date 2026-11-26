"""Chẩn đoán sai số (phần dư) của mô hình dự báo.

Sai số = giá trị thực - giá trị dự báo, thu được từ chính quá trình
rolling-origin (mỗi lần dự báo cho một sai số).

Hai câu hỏi chính:
  1. Sai số có bị lệch một phía không? (trung bình khác 0 -> lệch hệ thống)
  2. Sai số các tháng liền nhau có liên quan nhau không? (tự tương quan)
     Nếu có, nghĩa là mô hình còn bỏ sót quy luật nào đó.
"""
import numpy as np


def rolling_origin_errors(y, model_factory, h=1, min_train=60):
    """Trả về mảng sai số (thực tế - dự báo) của từng lần dự báo, tầm h."""
    y = np.asarray(y, dtype=float)
    errors = []
    for origin in range(min_train, len(y) - h + 1):
        model = model_factory().fit(y[:origin])
        errors.append(y[origin + h - 1] - model.predict(h)[-1])
    return np.array(errors)


def autocorrelation(errors, max_lag=12):
    """Hệ số tự tương quan của sai số ở độ trễ 1, 2, ..., max_lag."""
    e = np.asarray(errors, dtype=float)
    e = e - e.mean()
    denom = np.sum(e ** 2)
    if denom == 0:
        return np.zeros(max_lag)
    return np.array(
        [np.sum(e[k:] * e[: len(e) - k]) / denom for k in range(1, max_lag + 1)]
    )


def residual_summary(errors, max_lag=12):
    """Tóm tắt sai số: trung bình, độ lệch chuẩn, tự tương quan lag 1 và lag 12."""
    e = np.asarray(errors, dtype=float)
    acf = autocorrelation(e, max_lag)
    return {
        "n": len(e),
        "trung_binh": e.mean(),
        "do_lech_chuan": e.std(ddof=1),
        "mae": np.mean(np.abs(e)),
        "acf_lag1": acf[0],
        "acf_lag12": acf[max_lag - 1],
        "nguong_acf": 1.96 / np.sqrt(len(e)),  # ngoài ±ngưỡng này là đáng chú ý
    }