
from plates import is_valid


def main():
    test_two_letters()
    test_max_char()
    test_min_char()
    test_first_num()
    test_end_num()
    test_no_punc()
    test_begin_alpha()


def test_two_letters():
    assert is_valid("CS50") == True


def test_max_char():
    assert is_valid("OUTATIME") == False


def test_min_char():
    assert is_valid("H") == False


def test_first_num():
    assert is_valid("CS05") == False


def test_end_num():
    assert is_valid("CS50P") == False


def test_no_punc():
    assert is_valid("PI3.14") == False


def test_begin_alpha():
    assert is_valid("50") == False
