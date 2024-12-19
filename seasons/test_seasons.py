# Either before or after you implement seasons.py, additionally implement, in a file called test_seasons.py,
# one or more functions that test your implementation of any functions besides main in seasons.py thoroughly,
# each of whose names should begin with test_ so that you can execute your tests with pytest.

# Note to self: When testing an error, use with pytest.raises, and import pytest
# Cannot assert a ValueError

from seasons import date_delta, delta_to_words, DOB
import pytest
from datetime import date, timedelta

def test_dob():
    dob = DOB("1999-01-01")
    assert dob.year == 1999
    assert dob.month == 1
    assert dob.day == 1

def test_dob_invalid():
    with pytest.raises(SystemExit):
        DOB("cats")
    with pytest.raises(SystemExit):
        DOB("1999-1-1")
    with pytest.raises(SystemExit):
        DOB("1999")
    with pytest.raises(SystemExit):
        DOB("1999-15-01")
    with pytest.raises(SystemExit):
        DOB("1999-1-35")
    with pytest.raises(SystemExit):
        DOB("1999-01-")
    with pytest.raises(SystemExit):
        DOB("1999-1-01")

def test_date_delta():
    today = date.today()
    delta = date_delta(2000, 10, 1)
    expected_delta = int((today - date(2000, 10, 1)) / timedelta(minutes=1))
    delta == expected_delta


