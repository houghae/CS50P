# Promt user for their date of birth in YYYY-MM-DD format and then prints how old they are in minutes, rounded to the nearest integer, using English words.
# Assume that the user was born at midnight (i.e., 00:00:00) on that date.
# Assume that the current time is also midnight. In other words, even if the user runs the program at noon, assume that it’s actually midnight, on the same date.
# Use datetime.date.today to get today’s date
# Structure your program per the below, not only with a main function but also with one or more other functions as well.
# You’re welcome to import other (built-in) libraries, or any that are specified in the below hints.
# Exit via sys.exit if the user does not input a date in YYYY-MM-DD format. Ensure that your program will not raise any exceptions.
import re
import sys
from datetime import date, timedelta
import inflect
p = inflect.engine()

# Create dob class with year, month, day
# Add error handling to instance method
class DOB:
    def __init__(self, user_input):


    @classmethod
    def get(cls):
        user_input = input("Date of Birth: ").strip()
        return cls(user_input)


    @property
    def dob(self):
        return self._dob

    # error checking
    @dob.setter
    def dob(self, user_input):
        if dob := re.match(r"^([0-9]{4})-([0-9]{2})-([0-9]{2})$", user_input):
            year, month, day = dob.groups()
            year = int(year)
            month = int(month)
            day = int(day)
            try:
                date(year, month, day) == True
                pass
            except ValueError:
                sys.exit
        else:
            sys.exit

        self.year = year
        self.month = month
        self.day = day

def main():
    dob = DOB.get()
    num = date_delta(dob.year, dob.month, dob.day)
    print(f"{delta_to_words(num)} minutes")

# Create function to collect DOB input, do re.match to validate proper numerical format.
# Return year, month, day int variables. Moved to class.



# Create function that inputs user date, creates today's date, and returns the delta.
def date_delta(year, month, day):
    todays_date = date.today()
    user_date = date(year, month, day)
    date_delta = todays_date - user_date
    # This prints the delta variable in minutes
    return int(date_delta / timedelta(minutes=1))


# Create function that inputs numerical minutes and returns word minutes.
def delta_to_words(num_min):
    word_minutes = p.number_to_words(num_min)
    return word_minutes.replace("and ", "").capitalize()


if __name__ == "__main__":
    main()
