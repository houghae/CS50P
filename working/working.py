# PROGRAM SCOPE___________________________________________________________________________________________________________________________________________________________
# Structure working.py as follows, wherein you’re welcome to modify main and/or implement other functions as you see fit,
# but you may not import any other libraries. You’re welcome, but not required, to use re and/or sys.

# Implement a function called convert that expects a str in either of the 12-hour formats below and returns the corresponding str in 24-hour format (i.e., 9:00 to 17:00).
# Expect that AM and PM will be capitalized (with no periods therein) and that there will be a space before each.
# Input structured like this:
    # 9:00 AM to 5:00 PM
    # 9 AM to 5 PM
# Output structured like this:
    # 00:00 to 23:59
# Raise a ValueError instead if the input to convert is not in either of those formats or if either time is invalid (e.g., 12:60 AM, 13:00 PM, etc.).
# But do not assume that someone’s hours will start ante meridiem and end post meridiem; someone might work late and even long hours (e.g., 5:00 PM to 9:00 AM).
#_________________________________________________________________________________________________________________________________________________________________________
# Note to self: I felt the most confident thus far writing this program and it appears to be the cleanest and most concise to date. Regexes are actually pretty fun,
# and the logic of nesting functions within functions has really clicked.

import re

def main():
    print(convert(input("Hours: ")))


def convert(s):
    # group(1) == hours, group(2) == min, group(3) == AM/PM. Repeat for groups 4, 5, 6 respectively.
    # group 2 and 4 could be None or populated with minutes
    if input_time := re.search(r"^(1[0-2]|[1-9])(?::([0-5][0-9]))?(?: )(AM|PM)(?: to )(1[0-2]|[1-9])(?::([0-5][0-9]))?(?: )(AM|PM)$", s):
        start_hours, start_min, start_ampm, finish_hours, finish_min, finish_ampm = input_time.groups()
        start_h24 = hour_convert(start_hours, start_ampm)
        start_m24 = minute_convert(start_min)
        finish_h24 = hour_convert(finish_hours, finish_ampm)
        finish_m24 = minute_convert(finish_min)
        return f"{start_h24:02}:{start_m24:02} to {finish_h24:02}:{finish_m24:02}"
    else:
        raise ValueError


def hour_convert(hours, ampm):
    if ampm == "PM" and hours != "12":
        return int(hours) + 12
    if ampm == "PM" and hours == "12":
        return 12
    if ampm == "AM" and hours != "12":
        return int(hours)
    if ampm == "AM" and hours == "12":
        return 0


def minute_convert(min):
    if min == None:
        return 0
    else:
        return int(min)


if __name__ == "__main__":
    main()
