# Either before or after you implement convert in working.py, additionally implement, in a file called test_working.py,
# three or more functions that collectively test your implementation of convert thoroughly,
# execute your tests with pytest
#______________________________________________________________________________________________________________________
# Note to self: When testing an error, use with pytest.raises, and import pytest
# Cannot assert a ValueError

from working import convert
import pytest


def test_12():
    assert convert("12 AM to 12 PM") == "00:00 to 12:00"
    assert convert("12:00 AM to 12:00 PM") == "00:00 to 12:00"


def test_only_hours():
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"
    assert convert("10 PM to 8 AM") == "22:00 to 08:00"


def test_hours_min():
    assert convert("9:00 AM to 5:00 PM") == "09:00 to 17:00"
    assert convert("10:30 PM to 8:50 AM") == "22:30 to 08:50"


def test_value_error():
    # Each convert() call needs it's own with block. If not it'll catch the first exception and skip the rest.
    with pytest.raises(ValueError):
        convert("9:60 AM to 5:60 PM")
    with pytest.raises(ValueError):
        convert("9 AM - 5 PM")
    with pytest.raises(ValueError):
        convert("09:00 AM - 17:00 PM")
    with pytest.raises(ValueError):
        convert("9 AM5 PM")
    with pytest.raises(ValueError):
        convert("16:300 AM to 80:65 PM")


def test_str():
    with pytest.raises(ValueError):
        convert("cat AM to dog PM")
    with pytest.raises(ValueError):
        convert("cat")
    with pytest.raises(ValueError):
        convert("cat 9 AM to 5 PM")
    with pytest.raises(ValueError):
        convert("9 AM to 5 PM cat")




