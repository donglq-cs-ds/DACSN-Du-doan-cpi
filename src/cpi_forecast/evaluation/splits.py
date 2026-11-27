"""Chia dữ liệu theo thứ tự thời gian."""
import numpy as np


def time_train_test_split(y, test_size):
    """Chia chuỗi thành train (phần đầu) và test (test_size phần tử CUỐI).

    Không xáo trộn: test luôn nằm SAU train theo thời gian.
    """
    y = np.asarray(y, dtype=float)
    if test_size <= 0 or test_size >= len(y):
        raise ValueError("test_size phải nằm trong khoảng (0, len(y))")
    train = y[: -test_size]
    test = y[-test_size:]
    return train, test