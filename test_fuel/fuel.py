# Prompt user for fraction, formatted as X/Y
# Output percentage rounded to nearest integer
def main():
    userInput = input("Input fraction: ")
    fraction = convert(userInput)
    print(gauge(fraction))


# If, though, X or Y is not an integer, X is greater than Y, or Y is 0, instead prompt the user again
def convert(fraction):
    numerator, denominator = fraction.split("/")
    if numerator.isdigit() and denominator.isdigit() and int(numerator) <= int(denominator):
        percentage = round(int(numerator) / int(denominator), 2)
        return percentage * 100
    elif int(denominator) == 0:
        raise ZeroDivisionError
    elif numerator.isdigit() or denominator.isdigit() is False:
        raise ValueError
    elif int(numerator) > int(denominator):
        raise ValueError


# If 1% or less, output E
# If 99% or more, output F
def gauge(i):
    if i <= 1:
        return "E"
    elif i >= 99:
        return "F"
    else:
        return f"{int(i)}%"


if __name__ == "__main__":
    main()

