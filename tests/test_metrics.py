import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from cpi_forecast.evaluation.metrics import mae, mape  # noqa: E402


def test_mae_mape_vi_du_tinh_tay():
    y_true = np.array([100.0, 200.0])
    y_pred = np.array([110.0, 180.0])
    # sai lệch là 10 và 20  ->  MAE = 15
    # sai lệch tương đối là 10% và 10%  ->  MAPE = 10
    assert np.isclose(mae(y_true, y_pred), 15.0)
    assert np.isclose(mape(y_true, y_pred), 10.0)