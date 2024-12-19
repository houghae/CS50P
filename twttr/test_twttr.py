
from twttr import shorten


def main():
    testA()
    testE()
    testI()
    testO()
    testU()
    testUpper()
    testLower()
    testNum()
    testPunc()


def testA():
    assert shorten("AB") == "B"
    assert shorten("ab") == "b"


def testE():
    assert shorten("EB") == "B"
    assert shorten("eb") == "b"


def testI():
    assert shorten("IB") == "B"
    assert shorten("ib") == "b"


def testO():
    assert shorten("OB") == "B"
    assert shorten("ob") == "b"


def testU():
    assert shorten("UB") == "B"
    assert shorten("ub") == "b"


def testUpper():
    assert shorten("BAEIOURB") == "BRB"


def testLower():
    assert shorten("baeiourb") == "brb"


def testNum():
    assert shorten("12baeiourb90") == "12brb90"


def testPunc():
    assert shorten("12baeiourb90?") == "12brb90?"


if __name__ == "__main__":
    main()
