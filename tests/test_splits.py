"""Đảm bảo tập test luôn nằm sau tập train."""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))


def test_placeholder():
    assert True
