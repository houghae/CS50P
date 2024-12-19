# Instructions____________________________________________________________________________________________
# Create a program that uses the validator-collection library.
# Prompt user for email address via input and then print Valid or Invalid whether it's syntacically valid.
# Do not use re, do not check actual domain.
#_________________________________________________________________________________________________________

from validator_collection import validators, errors


def main():
    print(validate(input("Email: ")))


def validate(i):
    try:
        if validators.email(i):
            return "Valid"
        else:
            return "Invalid"
    except errors.InvalidEmailError:
        return "Invalid"
    except errors.EmptyValueError:
        return "Invalid"


if __name__ == "__main__":
    main()
