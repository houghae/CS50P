from datetime import date, timedelta

todays_date = date.today()

dob = date(1933, 1, 7)

delta = todays_date - dob



#print(todays_date)
#print(dob)
#print(delta)
print(delta.total_seconds())
print(delta / timedelta(seconds=1))

# This prints the delta variable in minutes
print(delta / timedelta(minutes=1))
