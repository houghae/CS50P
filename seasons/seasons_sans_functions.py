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




# Get a DOB input
# Do data scrubbing and error checking to make sure it's in the correct format. Use regex
    # If yes, return DOB to another function
    # If no, sys.exit
# Get current date
# Subtract DOB from current date
    # Create method to do this, I think. See hints.
    # Return delta in minutes
# Use inflect to convert delta to words
    # Might have to use multiple inflect methods or parameters to get to the right version of minutes



def main():
    user_input = input("Date of Birth: ").strip()
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

    todays_date = date.today()
    user_date = date(year, month, day)
    date_delta = todays_date - user_date

    # This prints the delta variable in minutes
    delta_minutes = date_delta / timedelta(minutes=1)
    delta_minutes = int(delta_minutes)
    word_minutes = p.number_to_words(delta_minutes)
    word_minutes = word_minutes.replace("and ", "").capitalize()


    print(f"{word_minutes} minutes")



if __name__ == "__main__":
    main()
