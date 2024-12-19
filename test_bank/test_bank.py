
from bank import value

def main():
    test_hello()
    test_hello_newmman()
    test_how_you_doing()
    test_whats_happening()


def test_hello():
    assert value("hello") == 0


def test_hello_newmman():
    assert value("hello, Newman") == 0


def test_how_you_doing():
    assert value("Hows it going?") == 20


def test_whats_happening():
    assert value("What's happening?") == 100


if __name__ == "__main__":
    main()
