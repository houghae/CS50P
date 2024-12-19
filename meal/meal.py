# Ask user for time input, call convert function, compare times, print if time to eat.
def main():
    t = input("What time is it?  ")
    t = convert(t)
    if 7.0 <= t <= 8.0:
        print("breakfast time")
    elif 12.0 <= t <= 13.0:
        print("lunch time")
    elif 18.0 <= t <= 19.0:
        print("dinner time")


# Converts time input to float in 12hr or 24hr format. This seems clunky AF.
def convert(time):
    time = time.strip()
    if (time.endswith("a.m.") and not time.startswith("12")) or (time.startswith("12") and time.endswith("p.m.")):
        time = time.replace("a.m.", "")
        time = time.replace("p.m.", "")
        hoursAM, minutesAM = time.split(":")
        return (float(hoursAM) + float(minutesAM)/60)
    elif (time.endswith("p.m.") and not time.startswith("12")) or (time.startswith("12") and time.endswith("a.m.")):
        time = time.replace("p.m.", "")
        time = time.replace("a.m.", "")
        hoursPM, minutesPM = time.split(":")
        hoursPM = float(hoursPM) + 12
        return (hoursPM + float(minutesPM)/60)
    else:
        hours24, minutes24 = time.split(":")
        return (float(hours24) + float(minutes24)/60)


if __name__ == "__main__":
    main()
