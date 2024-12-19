# Ask user for time input, call convert function, compare times, print if time to eat
def main():
    t = input("What time is it?  ")
    t = convert(t)
    if 7 <= t <= 8:
        print("breakfast time")
    elif 12 <= t <= 13:
        print("lunch time")
    elif 18 <= t <= 19:
        print("dinner time")


# Converts time input to float in 24 hr format
def convert(time):
    hours, minutes = time.strip().split(":")
    return (float(hours) + float(minutes)/60)


if __name__ == "__main__":
    main()
