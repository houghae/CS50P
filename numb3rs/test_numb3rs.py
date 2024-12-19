from numb3rs import validate

def main():
    test_0()
    test_i()
    test_ii()
    test_iii()
    test_too_large()
    test_str()
    test_incomplete()


def test_0():
    assert validate("0.0.0.0") == True


def test_i():
    assert validate("1.1.1.1") == True
    assert validate("9.9.9.9") == True


def test_ii():
    assert validate("42.42.42.42") == True
    assert validate("99.0.9.1") == True


def test_iii():
    assert validate("255.100.10.0") == True
    assert validate("255.255.255.255") == True


def test_too_large():
    assert validate("256.255.255.255") == False
    assert validate("255.256.255.255") == False
    assert validate("255.255.256.255") == False
    assert validate("255.255.255.256") == False
    assert validate("999.1.1.1") == False
    assert validate("1000.1.1.1") == False


def test_str():
    assert validate("c.a.t.s") == False
    assert validate("cats") == False


def test_incomplete():
    assert validate("42.") == False
    assert validate(".1.1.1") == False


if __name__ == "__main__":
    main()
