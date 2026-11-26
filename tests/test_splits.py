import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from cpi_forecast.evaluation.splits import time_train_test_split  # noqa: E402


def test_test_nam_sau_train():
    y = np.arange(10)                       # 0, 1, ..., 9
    train, test = time_train_test_split(y, test_size=3)
    assert list(train) == [0, 1, 2, 3, 4, 5, 6]
    assert list(test) == [7, 8, 9]
    assert train.max() < test.min()         # train luôn trước test
    assert len(train) + len(test) == len(y)