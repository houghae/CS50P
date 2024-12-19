
from fuel import convert, gauge
import pytest


def main():
    test_percent()
    test_not_int()
    test_num_too_large()
    test_denom_is_zero()
    test_gauge_e()
    test_gauge_f()
    test_gauge_z()


def test_percent():
    assert convert("1/2") == 50
    assert convert("1/10") == 10
    assert convert("9/10") == 90
    assert convert("1/100") == 1


def test_not_int():
    with pytest.raises(ValueError):
        convert("cat/dog")
        convert("cat/1")
        convert("1/dog")
        convert(".5/2")


def test_num_too_large():
    with pytest.raises(ValueError):
        convert("2/1")
        convert("100/1")


def test_denom_is_zero():
    with pytest.raises(ZeroDivisionError):
        convert("1/0")


def test_gauge_e():
    assert gauge(1) == "E"
    assert gauge(0) == "E"


def test_gauge_f():
    assert gauge(99) == "F"
    assert gauge(100) == "F"


def test_gauge_z():
    assert gauge(25) == "25%"
    assert gauge(52) == "52%"
    assert gauge(2) == "2%"
    assert gauge(98) == "98%"


if __name__ == "__main__":
    main()
