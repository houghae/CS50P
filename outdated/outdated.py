months = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}


# implement a program that prompts the user for a date, in month-day-year order, formatted like 9/8/1636 or September 8, 1636,
# If the user’s input is not a valid date in either format, prompt the user again. Assume that every month has no more than 31 days
def main():
    while True:
        # Prompt user for input
        userDate = input("Date: ")
        # Assign list variable and split input into month, day, year using /
        if "/" in userDate:
            userList = userDate.split("/")
            try:
                if int(userList[0]) <= 12 and len(userList) <= 3 and int(userList[1]) <= 31:
                    break
                else:
                    pass
            except ValueError:
                pass
        # Assign list variable and split input into month, day, year using " ". Remove , in day
        elif ", " in userDate:
            userList = userDate.replace(",", "").split(" ")
            if userList[0] in months and len(userList) <= 3 and int(userList[1]) <= 31:
                # Assign month the month value
                userList[0] = months[userList[0]]
                break
            else:
                pass
        else:
            pass
    formatDate(userList)


# print date in YYYY-MM-DD format
# Index the list variable to print year, month, day
# Format with leading zeros
def formatDate(i):
    year = int(i[2])
    month = int(i[0])
    day = int(i[1])
    print(f"{year}-{month:02}-{day:02}")


main()

