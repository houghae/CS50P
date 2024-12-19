#Takes in meal amount, tip percentage. Outputs tip amount.
def main():
    dollars = dollars_to_float(input("How much was the meal? "))
    percent = percent_to_float(input("What percentage would you like to tip? "))
    tip = dollars * percent
    print(f"Leave ${tip:.2f}")


#Accept string such as $##.## as input. Return ##.# as float.
def dollars_to_float(d):
    d = float(d.replace("$", ""))
    return float((f"{d:.1f}"))



#Accept string such as ##% as input. Return 0.## as float.
def percent_to_float(p):
    p = float(p.replace("%", ""))/100
    return float((f"{p:.2f}"))


main()
