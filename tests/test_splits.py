"""Đảm bảo tập test luôn nằm sau tập train."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from cpi_forecast.evaluation.splits import time_train_test_split  # noqa: E402


def test_test_nam_sau_train():
    y = np.arange(10.0)  # 0, 1, ..., 9 (giá trị tăng dần = thứ tự thời gian)
    train, test = time_train_test_split(y, test_size=3)
    assert list(train) == [0, 1, 2, 3, 4, 5, 6]
    assert list(test) == [7, 8, 9]
    assert train.max() < test.min()       # mọi điểm test đến SAU mọi điểm train
    assert len(train) + len(test) == len(y)


def test_test_size_khong_hop_le():
    with pytest.raises(ValueError):
        time_train_test_split(np.arange(5.0), test_size=5)