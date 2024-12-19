# Either before or after you implement count in um.py, additionally implement, in a file called test_um.py,
# three or more functions that collectively test your implementation of count thoroughly,
# each of whose names should begin with test_ so that you can execute your tests with pytest

from um import count

def test_word():
    assert count("um") == 1
    assert count("Um") == 1
    assert count("Um ") == 1
    assert count("Um?") == 1
    assert count(" Um") == 1
    assert count(", Um") == 1
    assert count("UM!") == 1


def test_string():
    assert count("Um, what's your name umpire?") == 1
    assert count("Humpty dumpty sat on a...um, wall") == 1
    assert count("Um, ho hum") == 1
    assert count("Um, thanks, um...") == 2
    assert count("Um, I have no idea, um, what we're um talking about umpire") == 3


def test_null():
    assert count("yum") == 0
    assert count("umpire") == 0
    assert count("humpty dumpty, uuuuuuuummmmmmmmmm") == 0
    assert count("hum") == 0


