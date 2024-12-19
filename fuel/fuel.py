# Prompt user for fraction, formatted as X/Y
# Output percentage rounded to nearest integer
def main():
    fraction = getFraction()
    print(showPercentage(fraction))


# If, though, X or Y is not an integer, X is greater than Y, or Y is 0, instead prompt the user again
def getFraction():
    while True:
        userInput = input("Input fraction: ")
        try:
            numerator, denominator = userInput.split("/")
            if numerator.isdigit() and denominator.isdigit() and int(numerator) <= int(denominator):
                return round(int(numerator) / int(denominator), 2)
        except (ValueError, ZeroDivisionError):
            pass
        else:
            pass


# If 1% or less, output E
# If 99% or more, output F
def showPercentage(x):
    x = x * 100
    if x <= 1:
        return ("E")
    elif x >= 99:
        return ("F")
    else:
        return f"{int(x)}%"


main()
