from jar import Jar
import pytest


def test_init():
    jar = Jar(15)
    assert jar.capacity == 15
    assert jar.size == 0
    jar2 = Jar()
    assert jar2.capacity == 12
    with pytest.raises(ValueError):
        jar3 = Jar(-1)


def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(1)
    assert str(jar) == "🍪"
    jar.deposit(11)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"


def test_deposit():
    jar = Jar(15)
    jar.deposit(10)
    assert jar.size == 10
    with pytest.raises(ValueError):
        jar.deposit(6)


def test_withdraw():
    jar = Jar(10)
    jar.deposit(2)
    jar.withdraw(2)
    assert jar.size == 0
    with pytest.raises(ValueError):
        jar.withdraw(5)
