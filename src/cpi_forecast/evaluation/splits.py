"""Chia dữ liệu theo thứ tự thời gian."""
import numpy as np


def time_train_test_split(y, test_size):
    """Chia train/test, test luôn nằm SAU train (không xáo trộn)."""
    y = np.asarray(y)
    train = y[:-test_size]     # tất cả, trừ test_size phần tử cuối
    test = y[-test_size:]      # test_size phần tử cuối
    return train, test